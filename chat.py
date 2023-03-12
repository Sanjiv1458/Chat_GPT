from flask import Flask, request, render_template, Markup
import openai
from lxml import html, etree


app = Flask(__name__)

# Set OpenAI API key
openai.api_key = "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"

# Set OpenAI GPT-3 model ID
model_engine = "text-davinci-003"

def is_html(text):
    try:
        parser = etree.HTMLParser()
        root = etree.fromstring(text, parser)
        return True
    except:
        return False

# Define route for home page
@app.route("/")
def home():
    return render_template("home.html")

# Define route for generating text
@app.route("/generate_text", methods=["POST"])
def generate_text():
    # Get prompt text from form
    prompt = request.form["prompt"]

    # Use OpenAI's GPT API to generate text
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    if(is_html(response) == True):
        result = html.document_fromstring(response.choices[0].text.strip())
        return render_template("results.html", Markup(html=etree.tostring(result, pretty_print=True, encoding='unicode')))
    else:
    # Render results template with generated text
        return render_template("results.html", text=response.choices[0].text.strip())


if __name__ == "__main__":
    app.run(debug=True)
