from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response
from app.Dependencies.dependencies import  get_topic_model

visualiseRouter=APIRouter(prefix="/visualise")


@visualiseRouter.get("/")
def visualiseTopics(topic_model = Depends(get_topic_model)):
    fig = topic_model.visualize_topics(custom_labels=True)
    html_str = fig.to_html(full_html=False)
    return Response(content=html_str, media_type="text/html")


