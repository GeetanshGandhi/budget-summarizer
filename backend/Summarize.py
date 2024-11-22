"""
Problem Statement :
Analyzing large documents like the Union Budget of India is a complex task due their large volume and time consuming nature.
Manual analysis can lead to delays and sometimes errors. Thus, there is a need for an automated tool that can efficiently summarize
the entire budget providing a quick and accurate insight, thereby facilitating timely decision-making.

"""
import google.generativeai as genai
import PyPDF2
#configure Gemini AI
genai.configure(api_key="************************") #YOUR API KEY HERE
model = genai.GenerativeModel("gemini-1.5-flash")

valueToPdfMap = {
##    "2024-25":"2024_25",
##    "2023-24":"2023_24",
##    "2022-23":"2022_23",
##    "2021-22":"2021_22",
##    "2020-21":"2020_21",
##    "2019-20":"2019_20",
##    "2018-19":"2018_19",
##    "2017-18":"2017_18",
##    "2016-17":"2016_17"
    }
for year in valueToPdfMap.keys():
    #fetching text to summarize from a PDF
    text = ""
    pdfReader = PyPDF2.PdfReader('E:/coding/WEB DEV/Budget_Summarizer/backend/BudgetPDFs/bs'+valueToPdfMap[year]+'.pdf')
    pages = pdfReader.pages

    for i in range(len(pages)):
        text+=pages[i].extract_text()+" "

    #prompting gemini for summarization
    prompt = """Content of a PDF file is given as text in the prompt ahead. 
    You need to summarize the following text. the summary must be divided into different sectors of economy,
    like Agriculture, health, education, etc. The PDF also contains taxation system.
    You have to present that as well. Output must be a JSON object parsed into a string in a single line, where key of each
    element of list would be the sub-category and the  would be a list of strings, denoting the summary for 
    the corresponding sub-category. Each bullet point must state a fact derived from the sentence in the speech and must be in third person grammar.
    The facts must not be in "first person" language and must be short and precise and MUST ONLY FOCUS ON
    statistical and numerical data present in the PDF. The first fact MUST be the budget alloted to the corresponding sector.
    Limit the number of facts to exactly 10 to make sure that ONLY NUMERICAL data is extracted. If the fact
    does not contain numerical data, discard it. NOTE that the output string will be parsed into json object as it is, thus the
    string must represent a valid JSON object and MUST NOT CONTAIN redundant backslashes and inverted commas"""
    
    response = model.generate_content([prompt, text]).text
    length = len(response)
    
    #feeding response to text file:
    writeToFile = open('E:/coding/WEB DEV/Budget_Summarizer/backend/Summaries/summary'+valueToPdfMap[year]+'.txt', 'w')
    #processing the text to write in text file
    for index in range(length):
        if response[index] != '`':
            if response[index] == "₹": writeToFile.write("Rs.")
            else:
                if response[index] == "\\" : continue
                if response[index] == '"':
                    if response[index-1] == ":" or response[index+1] == ":" or response[index-1] == "{" or response[index-1]=="[" \
                    or response[index+1]=="]" or response[index+1]=="," or response[index-2]=="," : writeToFile.write(response[index])
                else: writeToFile.write(response[index])
    print("Successfully written")

    writeToFile.close()
