import json
import openai


openai.api_key = ""


def lambda_handler(event, context):
    if not "answer" in event:
        return {
            'statusCode': 200,
            'body': json.dumps('Error: answer not found')
        }
    answer = event['answer']
    if len(answer)<50:
        return {
            'statusCode': 400,
            'body': json.dumps('Please try to make your response longer')
        }
    
    if not "question" in event:
        return {
            'statusCode': 200,
            'body': json.dumps('Error: question not found')
        }
    question = event['question']
    #### replace any ' or " in the question and answer with space
    
    
    prompt_prefix = """
    I will provide a paragraph which is output from a speech-to-text program. The paragraph is the answer to an IELTS speaking test question. The question and answer will be attached to the end for you to refer, 
    You should do the following things step by step:
    
    Step1: 
    Correct the misrecognized words and phrases accordingly.
    You will regard this answer as the tester's answer of this IELTS speaking test. Stoping using the raw answer for any evaluation but use the corrected version.
    
    Step2: 
    Give suggestions to improve the answer, ignore mistakes related to misrecognized words and punctuation, only list most useful ones.
    
    Step3:
    Regenerate an answer for the same question as a reference for user to learn from which have similar logic with the previous answer but performs better in IELTS test.
    
    Step4:
    Generate a related question to user to continue this conversation.
    
    Format your output like this:
    	
    
    1. ~~~~ Improvements could be made ~~~~
    	Put the most useful modifications and suggestions here
    	
    
    2. ~~~~ Similar answer for reference ~~~~
    	Put the answer you generated to better suit the test here
    	
    3. ~~~~ Next Question Recommendation ~~~~
        Put related question here
    
    """
    
    user_prompt = prompt_prefix + "Question: \n~~~\n" + question + "\n~~~\n" + " Raw Answer: \n~~~\n" + answer + "\n~~~\n"
    
    response = openai.ChatCompletion.create(
       model="gpt-4",
       messages=[
          {"role": "user", "content": user_prompt}
       ]
    )
    result_string = response.choices[0]["message"]["content"]

    return {
        'statusCode': 200,
        'body': json.dumps(result_string)
    }