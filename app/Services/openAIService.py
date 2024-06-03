class OpenAIService:
    def __init__(self, client):
        self.client = client
        self.context_template = """
            Your role is to enhance a query given by a user.
            This query is be a description of a new product/service that the user wants to market.
            The query should be enhanced, refined and very enriched (you should add more words that are relevant to the topic).
            The enhanced query is going to be used for a semantic search feature of influencers that can market the product.

            You are going to interact with the user and ask him questions to get more details on the topic of the product.
            Only ask questions that are relevant to the description of the topic of the product . 
            Never focus on the actual influencers, only focus on describing the product.

            Upon each user message, your output should only be a JSON document (NOT ANYTHING ELSE) composed of three keys:
                - irrelevant: a boolean representing that the query is irrelevant to the task at hand
                - enhanced_query: the current enhanced query
                - next_question: the next question you're going to ask the user

            If the query is not relevant to the tasks described above, please populate the irrelevant field with the value True and return your answer in the next_question field.
            If the user asks you to do something other than describing his product, apologize politely and say that you are incapable of performing that task.

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
            model="gpt-4o",
            response_format={ "type": "json_object" },

            messages=conversation
        )
        return response.choices[0].message.content
    def generate_title(self, message):
        conversation = [
            self.get_message('system', self.get_query({'query':message},"Generate a small title (max 3 words) for the converstation given the following user query: [QUERY]. Return a JSON with a unique attribute title")),
        ]

        return self.process_query(conversation)