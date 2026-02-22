from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import joblib
from process import process
from preprocessing import preprocessing

app = FastAPI()

model = joblib.load('artifacts/lr_model.pkl')
vectorizer = joblib.load('artifacts/vectorizer.pkl')

class AbstractClass(BaseModel):
    text: str


@app.post("/classical_predict")
async def classical_predict(data: AbstractClass):
    vec = vectorizer.transform([data.text])
    prob = model.predict_proba(vec)[0][1]
    label = int(prob>0.5)
    return {"malicious probability":float(prob), "prediction":label}


def transformer_predict(data):
    prob = process(data)
    if (prob['malicious_probability'] > 0.92):
        preprocessing(data, 1)
        return 403
    else:
        preprocessing(data, 0)
        return 200
    


@app.api_route("/ml_check", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def ml_check(request: Request):
    method = request.headers.get("x-original-method", "")
    path = request.headers.get("x-original-uri", "")
    user_agent = request.headers.get("user-agent", "")

    processed_log = f"{method} {path} {user_agent}"
    status = transformer_predict(processed_log)
    return Response(status_code=status)


