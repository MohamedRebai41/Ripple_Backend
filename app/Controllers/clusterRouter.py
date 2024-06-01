from fastapi import APIRouter, Body, Depends, HTTPException, Path
from app.Dependencies.dependencies import   get_pinecone_repository, get_topic_model
from app.Schemas.schemas import RenameTopicBody
from app.Services.pineconeRepository import PineconeRepository


clusterRouter=APIRouter(prefix="/clusters")


@clusterRouter.get("/")
def get_topics(topic_model = Depends(get_topic_model)):
    topics = topic_model.get_topic_info()
    filtered_df = topics[["Name","Representation","Count"]]
    topic_list = filtered_df.to_dict(orient="records")
    labels = topic_model.custom_labels_
    if(labels == None):
        return topic_list
    return [{"Name":label, "Keywords":topic["Representation"],"Count" :topic["Count"]} for label,topic in zip(labels,topic_list)]


@clusterRouter.post("/rename/{topic_id}")
def rename_topic(topic_id:int = Path(...,min=-1) ,name: RenameTopicBody = Body(...), topic_model = Depends(get_topic_model)):
    if(topic_id >= len(topic_model.custom_labels_) - 1):
        raise HTTPException(404,"Topic was not found!")
    topic_model.set_topic_labels({int(topic_id):name})   
    try:
        topic_model.push_to_hf_hub(
            repo_id="RebaiMed/Bertopic-Influencers",
            save_ctfidf=True
        )
    except:
        raise HTTPException(400,"Could not push to Hub")
    return True




@clusterRouter.get("/category/{influencer_id}")
def getCategory(influencer_id: str, pineconeRepository: PineconeRepository = Depends(get_pinecone_repository),topic_model = Depends(get_topic_model)):
    category_id = pineconeRepository.get_influencer_category(influencer_id)
    return {"category": topic_model.custom_labels_[int(category_id+1)]}



