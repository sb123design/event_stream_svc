# event_stream_svc
## How to Run
Run the requirements file to make sure the python packages are there:
`pip install -r requirements.txt`

In the base folder, run this command to start the service:
`uvicorn app.main:app --reload`

In a seperate terminal window, start adding some dummy data:
`curl -X POST http://127.0.0.1:8000/event \
  -H "Content-Type: application/json" \
  -d '{"metric": "temperature", "value": 1.3, "event_at": "2025-01-03"}'`

In another terminal window spin up the /stream endpoint and watch data come in as dummy data is added:
`curl 127.0.0.1:8000/stream`

Keep adding more dummy data with the POST call from above.

To test the history endpoint, change n to whatever number we want to return:
`curl "http://127.0.0.1:8000/history?n=2"`