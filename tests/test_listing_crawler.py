from jobmarket.crawler import find_job_links, find_next_page, parse_job_html


def test_itviec_job_urls_only():
    html = """
    <a href='/it-jobs/test-backend-1234?tracking=x'>Tin 1</a>
    <a href='/it-jobs/test-front-2345'>Tin 2</a>
    <a href='/it-jobs/python'>Bo loc khong phai tin</a>
    <a href='https://elsewhere.com/it-jobs/test-1234'>Khac domain</a>
    <a rel='next' href='/it-jobs?page=2'>Next</a>
    """
    links = find_job_links(html, 'https://itviec.com/it-jobs')
    assert links == [
        'https://itviec.com/it-jobs/test-backend-1234',
        'https://itviec.com/it-jobs/test-front-2345',
    ]
    assert find_next_page(html, 'https://itviec.com/it-jobs') == \
           'https://itviec.com/it-jobs?page=2'


def test_topcv_job_link():
    links = find_job_links(
        '<a href="/viec-lam/backend-developer/1234567.html?tracking=1">Backend</a>',
        'https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257')
    assert links == ['https://www.topcv.vn/viec-lam/backend-developer/1234567.html']


def test_careerviet_job_link():
    links = find_job_links(
        '<a href="/vi/tim-viec-lam/full-stack-developer.35C8D0B5.html">Developer</a>',
        'https://careerviet.vn/viec-lam/tat-ca-viec-lam-vi.html')
    assert links == ['https://careerviet.vn/vi/tim-viec-lam/full-stack-developer.35C8D0B5.html']

def test_careerviet_inferred_pagination_preserves_filter():
    first='https://careerviet.vn/viec-lam/cntt-phan-mem-c1-vi.html?sort=date'
    second='https://careerviet.vn/viec-lam/cntt-phan-mem-c1-trang-2-vi.html?sort=date'
    third='https://careerviet.vn/viec-lam/cntt-phan-mem-c1-trang-3-vi.html?sort=date'
    assert find_next_page('<html></html>',first)==second
    assert find_next_page('<html></html>',second)==third

def test_numeric_pagination_and_no_unrelated_link():
    html='<a href="/it-jobs?page=2">2</a><a href="https://evil.example/it-jobs?page=2">2</a>'
    assert find_next_page(html,'https://itviec.com/it-jobs')=='https://itviec.com/it-jobs?page=2'

def test_query_page_fallback_keeps_filters():
    assert find_next_page('', 'https://itviec.com/it-jobs?query=python&job_selected=abc') == 'https://itviec.com/it-jobs?query=python&page=2'
    assert find_next_page('', 'https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?foo=bar&page=2') == 'https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257?foo=bar&page=3'
    assert find_next_page('', 'https://www.topcv.vn/cong-ty/demo') is None

def test_topcv_and_itviec_visit_two_pages(monkeypatch):
    import jobmarket.crawler as c
    for base, paths in [
        ('https://itviec.com/it-jobs', ['/it-jobs/alpha-1234','/it-jobs/beta-5678']),
        ('https://www.topcv.vn/tim-viec-lam-cong-nghe-thong-tin-cr257', ['/viec-lam/alpha/123.html','/viec-lam/beta/456.html']),
    ]:
        seen=[]
        class Response:
            status_code=200
            def __init__(self,url):
                self.url=url
                if url == base: self.text=f'<a href="{paths[0]}">job</a>'
                elif url == base+'?page=2': self.text=f'<a href="{paths[1]}">job</a>'
                else: self.text='<script type="application/ld+json">{"@type":"JobPosting","title":"Developer","hiringOrganization":{"name":"Demo"}}</script>'
            def raise_for_status(self): pass
        class Session:
            def __init__(self): self.headers={}
            def get(self,url,timeout): seen.append(url); return Response(url)
        monkeypatch.setattr(c.requests,'Session',Session)
        monkeypatch.setattr(c,'_allowed',lambda *args: True)
        monkeypatch.setattr(c.time,'sleep',lambda _: None)
        rows,errors=c.crawl_urls([base],delay=1,max_jobs=0,max_pages=2)
        assert len(rows)==2 and not errors and base+'?page=2' in seen

def test_repeated_listing_stops_without_spinning(monkeypatch):
    import jobmarket.crawler as c
    class Response:
        status_code=200
        def __init__(self,url):
            self.url=url
            self.text='<a href="/vi/tim-viec-lam/demo.123.html">Developer</a>' if '/viec-lam/' in url else '<script type="application/ld+json">{"@type":"JobPosting","title":"Developer","hiringOrganization":{"name":"Demo"}}</script>'
        def raise_for_status(self): pass
    class Session:
        def __init__(self): self.headers={}
        def get(self,url,timeout): return Response(url)
    monkeypatch.setattr(c.requests,'Session',Session)
    monkeypatch.setattr(c,'_allowed',lambda *a: True)
    monkeypatch.setattr(c.time,'sleep',lambda _: None)
    records,errors=c.crawl_urls(['https://careerviet.vn/viec-lam/cntt-phan-mem-c1-vi.html'],1,10,0)
    assert len(records)==1 and any('khong co link moi' in e['reason'] for e in errors)


def test_detail_jsonld():
    html = '''<html><script type="application/ld+json">
    {"@context":"https://schema.org","@type":"JobPosting",
    "title":"Python Backend","hiringOrganization":{"name":"Example Corp"},
    "jobLocation":{"address":{"addressLocality":"Ha Noi"}},
    "baseSalary":{"currency":"VND","value":{"minValue":15000000,"maxValue":25000000}},
    "datePosted":"2026-11-17", "skills":["Python","SQL"]}
    </script></html>'''
    result = parse_job_html(html, 'https://itviec.com/it-jobs/python-backend-1234')
    assert result['company_name'] == 'Example Corp'
    assert result['salary_min'] == 15000000
    assert result['skills'] == 'Python, SQL'


def test_listing_to_details_without_internet(monkeypatch):
    import jobmarket.crawler as c

    listing = ("<a href='/it-jobs/python-1010'>Python</a>"
               "<a href='/it-jobs/java-2020'>Java</a>")
    def detail(title):
        return ("<script type='application/ld+json'>" +
                '{"@type":"JobPosting","title":"' + title +
                '","hiringOrganization":{"name":"Demo Company"}}' +
                '</script>')
    pages = {
        'https://itviec.com/robots.txt': 'User-agent: *\nAllow: /\n',
        'https://itviec.com/it-jobs': listing,
        'https://itviec.com/it-jobs/python-1010': detail('Python Developer'),
        'https://itviec.com/it-jobs/java-2020': detail('Java Developer'),
    }

    class Response:
        def __init__(self, url):
            self.status_code = 200
            self.url = url
            self.text = pages[url]
        def raise_for_status(self):
            pass

    class FakeSession:
        def __init__(self):
            self.headers = {}
        def get(self, url, timeout):
            return Response(url)

    monkeypatch.setattr(c.requests, 'Session', FakeSession)
    monkeypatch.setattr(c.time, 'sleep', lambda _: None)
    results, errors = c.crawl_urls(['https://itviec.com/it-jobs'], delay=1, max_jobs=2)
    assert not errors
    assert [r['job_title'] for r in results] == ['Python Developer', 'Java Developer']
    assert all(r['crawled_at'].endswith('Z') for r in results)
