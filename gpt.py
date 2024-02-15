import os
import time
from openai import OpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)


def get_prompt(question):
    try:
        # Create an assistant
        assistant = client.beta.assistants.create(
            name="Ai Lecturer",
            instructions="I'm a lecturer. I am here for students to explain topics that are confusing for them, not for cheating and writing their homeworks. I do not give them answers of exercise, i am trying to explain for them.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )

        # Create a new thread
        thread = client.beta.threads.create()

        # Send the question to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Execute the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        def wait_on_run(run, thread):
            while run.status == "queued" or run.status == "in_progress":
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id,
                )
                time.sleep(0.5)
            return run
        wait_on_run(run,thread)
        # time.sleep(10)
        # Get the last message from the thread which is assumed to be the answer
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        last_message = messages.data[0]
        response = last_message.content[0].text.value
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# if __name__ == "__main__":
#     while True:
#         user_input = input("Student: ")
#         if user_input.lower() in ["quit","exit","bye"]:
#             break
#
#         answer = get_prompt(user_input)
#         print(answer)
