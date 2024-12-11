from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from gen_ai_hub.proxy.langchain.init_models import init_llm

if __name__ == '__main__':


    llm = init_llm('gpt-4o')

    template = """Question: {question}
        Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=['question'])
    question = 'What is a supernova?'

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({'question': question})
    print(response)
