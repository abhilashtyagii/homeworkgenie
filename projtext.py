import gradio as gr 
import openai 
import re 
import warnings 
warnings.filterwarnings("ignore", message="Usage of gradio.inputs is deprecated") 
warnings.filterwarnings("ignore", message="`optional` parameter is deprecated") 
warnings.filterwarnings("ignore", message="`numeric` parameter is deprecated") 
 
# Set up your OpenAI API key 
openai.api_key = "Enter your key here." 
 
# Define a function that uses OpenAI's API to suggest questions based on the provided text 
def suggest_questions(text, max_questions=2): 
    # Clean the text of any unwanted characters 
    clean_text = re.sub('\n', ' ', text) 
 
    # Create the prompt for OpenAI's API 
    prompt = f"Please suggest {max_questions} questions that can be asked based strictly on the given text: {clean_text}\nQuestions:" 
 
    # Send the prompt to OpenAI's API 
    response = openai.Completion.create( 
        model="text-davinci-002", 
        prompt=prompt, 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.5 
    ) 
 
    # Extract the suggested questions from the API response 
    questions = response.choices[0].text.strip().split("\n") 
 
    # Return up to max_questions suggested questions 
    return questions[:max_questions] 
 
# Define a function that uses OpenAI's API to answer a user's question 
def ask_question(text, question): 
    # Clean the text of any unwanted characters 
    clean_text = re.sub('\n', ' ', text) 
 
    # Create the prompt by concatenating the question and the text 
    prompt = f"Given: {clean_text}, answer the following question only if it is available in the text. If the answer is not available within the text, respond with 'Answer not available within the text.'\n\nQuestion: {question}\nAnswer:" 
 
    # Send the prompt to OpenAI's API 
    response = openai.Completion.create( 
        model="text-davinci-002", 
        prompt=prompt, 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.5 
    ) 
 
    # Extract the answer from the API response 
    answer = response.choices[0].text.strip() 
 
    # Return the answer to the user 
    return answer 

# Define a function that uses OpenAI's API to suggest questions based on the provided text 
def ques_suggest_questions(text, question, max_questions=2): 
    # Clean the text of any unwanted characters 
    clean_text = re.sub('\n', ' ', text) 
 
    # Create the prompt for OpenAI's API 
    prompt = f"Please suggest {max_questions} questions based on the subject of the {question} asked in context to: {clean_text}\nQuestions:" 
 
    # Send the prompt to OpenAI's API 
    response = openai.Completion.create( 
        model="text-davinci-002", 
        prompt=prompt, 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.5 
    ) 
 
    # Extract the suggested questions from the API response 
    text_questions = response.choices[0].text.strip().split("\n") 
 
    # Return up to max_questions suggested questions 
    return text_questions[:max_questions] 
 
# Create a Gradio interface for the question answering bot 
def question_answering_bot(text, question): 
    # Get suggested questions based on the provided text 
    suggested_questions = suggest_questions(text, max_questions=2) 

    #Get suggest questions based on the provided subject in your asked question.
    ques_suggested_questions = ques_suggest_questions(text,question,max_questions=2)
 
    # Answer the user's question 
    answer = ask_question(text, question) 
 
    # Return the suggested questions and answer to the user 
    return answer,"\n ".join(suggested_questions),"\n".join(ques_suggested_questions),
 
interface = gr.Interface( 
    fn=question_answering_bot,  
    inputs=[ 
        gr.inputs.Textbox(label="Enter the text to be analyzed:"),  
        gr.inputs.Textbox(label="Enter a question:") 
    ],  
    outputs=[ 
        gr.outputs.Textbox(label="Answer:"),
        gr.outputs.Textbox(label="Suggested Questions:"),
        gr.outputs.Textbox(label = "What else you may ask related to your question:")
        ],
    title="Homework Genie",
    description="Enter some text, based on it ask a question and we'll help you get the answer.",
    examples=[["The name tiramisù comes from the Italian tiramisù, meaning “pick me up” or “cheer me up.” And that’s the perfect way to describe this rich and decadent Italian dessert. Some records state that Tiramisù originated in Treviso, Italy in 1800, but other records state that it originated from an idea by pastry chef Loly Linguanotto in the late 1960’s. Even though its exact origins have been debated, what we know for sure is that you’re going to love it.", "What is Tiramisu's origin country?"]]) 
 
interface.launch()
