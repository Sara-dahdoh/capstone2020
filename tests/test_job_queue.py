
"""
Test class for Job-Queue Class.
"""
import pytest
from c20_server.job_queue import JobQueue
from c20_server.job import Job, DocumentsJob
from c20_server import job_queue_errors


@pytest.fixture(name='job_queue')
def make_job_queue():
    return JobQueue()


@pytest.fixture(name='documents_job')
def make_first_documents_job():
    return DocumentsJob('job01', 1000, '2020-1-28', '2020-5-6')


def test_one_job_added_is_returned_by_get(job_queue):
    job = Job(1234)

    assert job_queue.get_num_unassigned_jobs() == 0
    job_queue.add_job(job)
    assert job_queue.get_num_unassigned_jobs() == 1
    assert job_queue.get_job() == job
    assert job_queue.get_num_unassigned_jobs() == 0


def test_add_two_jobs_then_remove_them(job_queue):
    job1 = Job(123411)
    job2 = Job(56722)

    job_queue.add_job(job1)
    job_queue.add_job(job2)
    assert job_queue.get_num_unassigned_jobs() == 2

    assert job_queue.get_job() == job1
    assert job_queue.get_job() == job2
    assert job_queue.get_num_unassigned_jobs() == 0


def test_get_one_job_from_empty_list(job_queue):
    with pytest.raises(job_queue_errors.NoJobsAvailableException):
        job_queue.get_job()


def test_one_documents_job_added_is_returned_by_get(job_queue, documents_job):

    job_queue.add_job(documents_job)
    assert job_queue.get_num_unassigned_jobs() == 1

    requested_job = job_queue.get_job()
    assert job_queue.get_num_unassigned_jobs() == 0

    assert requested_job.job_id == 'job01'
    assert requested_job.page_offset == 1000
    assert requested_job.start_date == '2020-1-28'
    assert requested_job.end_date == '2020-5-6'
