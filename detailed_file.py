import spacy
from sentence_transformers import SentenceTransformer,util
from paragraph_comparator import compare
import time

class DetailFileComparator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def file_detail_comparator(self, master_text, comparison_text):
        start = time.time()
        print("Detailed FIle comparision is started"+str(start))

        # nlp = spacy.load("en_core_web_sm")

        # print("line 37 - nlp load "+str(time.time()-start))

        master_doc = self.nlp(master_text)
        # print("line 40 - nlp load "+str(time.time()-start))


        comparison_doc = self.nlp(comparison_text)
        # print("line 44 - nlp load "+str(time.time()-start))


        def get_paragraphs(document):
            start = 0
            for token in document:
                if token.is_space and token.text.count("\n") > 1:
                    yield document[start:token.i]
                    start = token.i
            yield document[start:]

        master_doc_paras = list(get_paragraphs(master_doc))


        comparison_doc_paras = list(get_paragraphs(comparison_doc))


        # print(str(master_doc_paras))  

        model = SentenceTransformer('bert-base-nli-mean-tokens')
        # print("line 61 - nlp load "+str(time.time()-start))



        def cosineSimilarity(master_p, comaprison_p):
            similarity_results = []
            if(len(master_p) != len(comaprison_p)):
                length = len(master_p) - len(comaprison_p)
                if(length > 0):
                    comaprison_p.extend(['']*length)
                else:
                    master_p.extend(['']*abs(length))

            for i in range(len(master_p)):
                embeddings1 = model.encode(str(master_p[i]))
                local_similarity = []
                for j in range(len(master_p)):
                    embeddings2 = model.encode(str(comaprison_p[j]))
                    cosine_scores = util.pytorch_cos_sim(embeddings1, embeddings2)
                    local_similarity.append(cosine_scores.item())
        
                similarity_results.append(local_similarity)
                
            return similarity_results


        result = cosineSimilarity(master_doc_paras, comparison_doc_paras)
        # print(result)

        comparison_results = []

        # once we have got the result, we can check the highest matching para
        for master_para_index,para_score in enumerate(result):
            score = max(para_score)
            comparison_para_index = para_score.index(score)
            if(score >= 0.9999):
                comparison_results.append(
                    {
                        "p1":[{"tkn":str(master_doc_paras[master_para_index]),"cls":"gn"}],
                        "p2":[{"tkn":str(comparison_doc_paras[comparison_para_index]),"cls":"gn"}]
                    })
                # print("Paragraph master-> "+str(master_para_index) + " : comparison doc ->" +str(comparison_para_index)+" is a exact match no need to check")
            else:
                result = compare(master_doc_paras[master_para_index].text, comparison_doc_paras[comparison_para_index].text)
                comparison_results.append(result)
                # print("Paragraph master-> "+str(master_para_index) + " : comparison doc ->" +str(comparison_para_index)+" is not a exact match")

        # result_json = json.dumps(comparison_results)
        # with open("sample.json", "w") as outfile:
        #     outfile.write(result_json)
        print("Comparision result is ended"+str(time.time()-start))
        # return result_json
        return comparison_results
    
# obj =  DetailFileComparator()
# text1 = """Ratan Naval Tata (Ratan Ṭāṭā, born 28 December 1937) is an Indian industrialist, philanthropist, and a former chairman of Tata Sons. He was also been chairman of Tata Group, from 1990 to 2012, and again, as interim chairman, from October 2016 through February 2017, and continues to head its charitable trusts.[3][4] He is the recipient of two civilian awards of India, the Padma Vibhushan (2008), the second highest civilian honour, and the Padma Bhushan (2000), the third highest civilian honour.[5]

# Born in 1937, he is a scion of the Tata family, and son of Naval Tata who was later adopted by Ratanji Tata, son of Jamsetji Tata, the founder of Tata Group. He is an alumnus of the Cornell University College of Architecture and Harvard Business School through the Advanced Management Program that he completed in 1975.[6] He joined his company in 1961 when he used to work on the shop floor of Tata Steel, and was the apparent successor to J. R. D. Tata upon the latter's retirement in 1991. He got Tata Tea to acquire Tetley, Tata Motors to acquire Jaguar Land Rover, and Tata Steel to acquire Corus, in an attempt to turn Tata from a largely India-centrist group into a global business."""

# text2 = """Ratan Tata was born in Bombay, now Mumbai, during the British Raj on 28 December 1937,[7] and is the son of Naval Tata (born in Surat). His biological maternal grandmother had been the sister of Hirabai Tata, wife of group founder Jamsetji Tata. His biological grandfather, Hormusji Tata, had belonged to the broader Tata family; Ratan therefore was a Tata by birth. Parents Naval and Sonoo separated in 1948 when Ratan was 10, and he was subsequently raised by the widow of Sir Ratanji Tata, his grandmother, Navajbai Tata, who formally adopted him through the J. N. Petit Parsi Orphanage.[8] He has a half-brother, Noel Tata (from Naval Tata's second marriage with Simone Tata), with whom he was raised. His first language is Gujarati.[9]

# """

# print(obj.file_detail_comparator(text1,text2))