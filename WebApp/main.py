from flask import Flask, render_template,request
import os
import rake
import TextRank
import multi_senti_func


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/keyphrase_extraction")
def keyphrase_extraction():
    return render_template("keyphrase.html")
@app.route("/keyphrase_extraction/textrank")
def keyphrase_extraction_textrank():
    return render_template("textrank.html")

#yunsi
@app.route("/sentimental_analysis_multilingual")
def multilingual_analysis():
    return render_template("multi_senti.html")
#yunsi
@app.route("/get_senti_infor",methods=['POST'])
def get_senti_infor():
    text = request.form['text']
    title = request.form['title']
    #print("Get Form data")
    trans_text = multi_senti_func.translation_to_eng(text)
    trans_title = multi_senti_func.translation_to_eng(title)
    text_token = multi_senti_func.tokenization(trans_text)
    title_token = multi_senti_func.tokenization(trans_title)
    text_pos = multi_senti_func.pos_mark(text_token)
    title_pos = multi_senti_func.pos_mark(title_token)
    wn_text_senti_score = multi_senti_func.senti_score(text_pos)
    wn_title_senti_score = multi_senti_func.senti_score(title_pos)
    vander_text_senti_score = multi_senti_func.vader_senti_score(trans_text)
    vander_title_senti_score = multi_senti_func.vader_senti_score(trans_title)
    adjusted_score = multi_senti_func.adjusted_score(wn_text_senti_score,wn_title_senti_score,vander_text_senti_score,vander_title_senti_score)
    context = dict() #input back
    context['text'] = text #result
    context['title'] = title
    context['trans_text'] = trans_text #result
    context['trans_title'] = trans_title
    context['wn_text_senti_score']= wn_text_senti_score
    context['wn_title_senti_score']= wn_title_senti_score
    context['vander_text_senti_score']= vander_text_senti_score
    context['vander_title_senti_score']= vander_title_senti_score
    context['adjusted_score']= adjusted_score
    #print("Context: ",context)
    return render_template("multi_senti_score.html", **context)

#yunsi
@app.route("/survey_senti",methods=['POST'])
def survey_senti():
    before_sur = request.form['before_sur']
    after_sur = request.form['after_sur']
    #print("Get Form data")
    trans_bef = multi_senti_func.translation_to_eng(before_sur)
    trans_aft = multi_senti_func.translation_to_eng(after_sur)
    bef_token = multi_senti_func.tokenization(trans_bef)
    aft_token = multi_senti_func.tokenization(trans_aft)
    bef_pos = multi_senti_func.pos_mark(bef_token)
    aft_pos = multi_senti_func.pos_mark(aft_token)
    wn_bef_senti_score = multi_senti_func.senti_score(bef_pos)
    wn_aft_senti_score = multi_senti_func.senti_score(aft_pos)
    context = dict() #input back
    context['before_sur'] = before_sur #result
    context['after_sur'] = after_sur
    context['trans_bef'] = trans_bef #result
    context['trans_aft'] = trans_aft
    context['wn_bef_senti_score']= wn_bef_senti_score
    context['wn_aft_senti_score']= wn_aft_senti_score
    #print("Context: ",context)
    return render_template("multi_survey_score.html", **context)

@app.route('/get_keyphrases',methods=['POST']) #action
def get_keyphrases():
    stoppath = "SmartStoplist.txt"
    text=request.form['text'] #name
    min_char_length=request.form['min_char_length']
    min_words_length=request.form['min_words_length']
    max_words_length=request.form['max_words_length']
    min_keyword_frequency=request.form['min_keyword_frequency']
    trade_off=request.form['trade_off']
    top_n=request.form['top_n']
    rake_object = rake.Rake(stoppath,int(min_char_length),int(min_words_length),int(max_words_length),int(min_keyword_frequency),1,3,2)
    keywords_score, keywords_counts, stem_counts = rake_object.run(text, float(trade_off),int(top_n))
    context = dict() #input back
    context['keywords_score'] = keywords_score #result
    context['keywords_counts'] = keywords_counts
    context['stem_counts']= stem_counts
    return render_template("keyphrase_result.html", **context)

@app.route('/get_keyphrases_textrank',methods=['POST'])
def get_keyphrases_textrank():
    text=request.form['textrank_text']
    top_n=request.form['top_n_textrank']
    top_keywords=TextRank.extractKeyphrases(text,int(top_n))
    context=dict()
    context['keywords']=top_keywords
    return render_template("keyword_textrank.html",**context)

if __name__=="__main__":
    app.run(debug=True)
