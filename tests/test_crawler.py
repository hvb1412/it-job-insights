from pathlib import Path
from jobmarket.crawler import parse_job_html,crawl_offline_html


def test_jsonld_fixture():
    path=Path(__file__).parent/'fixtures'/'example_jobposting.html'
    found=parse_job_html(path.read_text(encoding='utf8'),'https://example.org/jobs/1')
    assert found['job_title']=='Python Backend Developer'
    assert found['company_name']=='Example Company (FICTIONAL)'
    assert found['salary_min']==20_000_000
    assert found['source']=='example.org'


def test_offline_fixture_not_live():
    records,errors=crawl_offline_html(Path(__file__).parent/'fixtures')
    assert len(records)==1 and not errors
    assert records[0]['source']=='offline_fixture'
