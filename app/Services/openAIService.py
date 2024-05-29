class OpenAIService:
    def __init__(self, client):
        self.client = client
        self.context_template = """
            Your role is to enhance a query given by a user.
            This query is a description of a new product/service that the user (the one who created the product) wants to market.
            The enhanced query is going to be used for a semantic search feature of influencers that can market the product.
            You are going to interact with the user and ask him questions to get more details on the product.
            Only ask questions that are relevant to the description of the product itself. 
            The query should be enhanced, refined and very enriched (add more words that are relevant to the topic) but should remain only a description of the product.
            Upon each user message, your output should be a JSON document composed of two keys:
                - enhanced_query: the current enhanced query
                - next_question: the next question you're going to ask the user
            Here is the initial query: [QUERY].
            Translate it to english if needed.
        """
    def get_query(self,data: dict, template: str):
        # Replace placeholders in the template with corresponding data from the dictionary
        for key, value in data.items():
            placeholder = f'[{key.upper()}]'
            query = template.replace(placeholder, value)
        return query
    
    def get_message(self,role,message):     
        return {'role':role, 'content':message}
    
    def get_start_message(self,input):
        return self.get_message('system',self.get_query({"query":input},self.context_template))

    def process_query(self, conversation):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        return response.choices[0].message.content