export FLASK_APP=app
export FLASK_DEBUG=True
export FLASK_ENVIRONMENT=debug
export DATABASE_URI="postgresql://postgres:pg123@localhost:5432/casting_test"
python -m unittest tests.test_suite