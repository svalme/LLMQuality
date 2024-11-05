import datetime

from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed to use session


questions = [
    "Laird: Pure research provides us with new technologies that contribute to saving lives. Even more worthwhile than this, however, is its role in expanding our knowledge and providing new, unexplored ideas. Kim: Your priorities are mistaken. Saving lives is what counts most of all. Without pure research, medicine would not be as advanced as it is.Laird and Kim disagree on whether pure research: (A) derives its significance from new technologies, (B) expands our knowledge of medicine, (C) should prioritize saving lives, (D) has its value in medical applications, or (E) has value only in providing technologies to save lives?",
    "Executive: We recently ran a set of advertisements in a travel magazine and on its website. We were unable to get direct information about consumer response to the print ads. However, we found that consumer response to the website ads was much more limited than typical. We concluded that consumer response to the print ads was probably below par. The executive’s reasoning does which one of the following? (A) base a prediction on information about intensity of a phenomenon’s cause, (B) use typical frequency to draw conclusions about a particular event, (C) infer a statistical generalization from specific instances, (D) use a case with direct evidence to draw conclusions about an analogous case, or (E) base a prediction on facts about recent comparable events?",
    "During the construction of the Quebec Bridge in 1907, designer Theodore Cooper learned of a downward deflection of the span. Before he could act, the cantilever arm broke, causing the worst construction disaster in history. The inquiry that followed changed the engineering rules of thumb used worldwide. Which one of the following can be inferred from the passage? (A) Bridges built before 1907 were unsafe due to lack of analysis, (B) Cooper’s absence caused the cantilever to break, (C) Engineers relied on rules of thumb due to inadequate methods, (D) Only rigorous analysis could have prevented the collapse, or (E) Prior to 1907, mathematical analysis was insufficient for safety.",
    "The supernova event of 1987 is notable for the absence of the neutron star that should have remained after such an explosion, despite extensive searches for its radiation. Thus, current theory claiming that certain supernovas always produce neutron stars is likely incorrect. Which one of the following strengthens the argument? (A) Most detected remnants have a nearby neutron star, (B) Neutron stars have been found farther away than the 1987 location, (C) The 1987 supernova was the first observed in progress, (D) Several features of the supernova match current theory, or (E) Some neutron stars arise from causes other than supernovae.",
    "Political scientist: Democracy does not promote political freedom; historical examples show democracies can lead to oppression, while some despotisms provide freedom. The reasoning is flawed because it (A) confuses necessary with sufficient conditions for freedom, (B) fails to consider that increased freedom might lead to more democracy, (C) appeals to irrelevant historical examples, (D) overlooks that democracy can promote freedom without being necessary or sufficient, or (E) bases its case on a personal viewpoint.",
    "Journalist: To balance the need for profits to support drug research with the moral imperative to provide medicines to those in need, some pharmaceutical companies sell drugs at high prices in rich nations and lower prices in poor ones. This practice is unjustified. Which principle most helps to justify the journalist’s reasoning? (A) The ill deserve more consideration than the healthy, (B) Wealthy institutions must use resources to assist the incapable, (C) Special consideration depends on needs rather than societal characteristics, (D) People in wealthy nations shouldn't have better healthcare than those in poorer nations, or (E) Unequal access to healthcare is more unfair than unequal wealth distribution.",
    "Several critics claim any contemporary poet writing formal poetry is performing a politically conservative act. This is false, as seen in poets like Molly Peacock and Marilyn Hacker, who are politically progressive feminists. The conclusion follows if which one of the following is assumed? (A) No feminist is politically conservative, (B) No poet writing unrhymed poetry is conservative, (C) No politically progressive person can perform a conservative act, (D) Anyone who writes non-conservative poetry never writes conservative poetry, or (E) The content of a poet’s work is the decisive factor for its political consequences.",
    "About two million years ago, lava dammed a river, creating a lake that existed for about half a million years. Bones of an early human ancestor were found in ancient sediments atop the lava layer. Therefore, ancestors of modern humans lived in western Asia between two million and one-and-a-half million years ago. Which assumption is required by the argument? (A) No other lakes existed in the area before the dam, (B) The lake had fish that human ancestors could eat, (C) The lava did not contain human fossils, (D) The lake was deep enough to drown in, or (E) The bones were in the sediments before the lake dried up.",
    "In jurisdictions where headlights are optional in good visibility, drivers using headlights all the time have fewer collisions than those using them only in poor visibility. Yet, mandatory use of headlights does not reduce overall collisions. Which one of the following resolves the discrepancy? (A) One in four drivers uses headlights in good weather where optional, (B) Making headlights mandatory is not difficult to enforce, (C) Only careful drivers use headlights when not required, (D) Some places prohibit headlights in good visibility, or (E) Mandatory use occurs where visibility is often poor.",
    "The Venetian Renaissance painter Vittore Carpaccio is known for using sumptuous reds. The recently discovered painting Erato Declaiming contains such reds, suggesting it is by Carpaccio. Which of the following contains a similar flawed reasoning pattern? (A) Most Renaissance painters worked in a single medium, (B) The Virgin and Child was the common subject in Italian painting, (C) Renaissance works were mostly commissioned, (D) St. Sebastian is likely early Florentine as it is in tempera, or (E) Late-Renaissance paintings were mostly in oil, suggesting Arnoldi painted in oil."
]

answers = {
    0: [
        " Laird and Kim have contrasting views on the value of pure research, with Laird focusing on the intrinsic worth of expanding knowledge and sparking new ideas, while Kim prioritizes its life-saving applications. Laird argues that pure research should not be confined to practical applications but valued for fostering intellectual growth. Kim, on the other hand, sees the life-saving potential of pure research as the most significant aspect. The correct answer is (C), as their disagreement fundamentally revolves around whether pure research should prioritize saving lives over advancing knowledge for its own sake.",
        "Laird and Kim’s debate revolves around the value of pure research, with Laird emphasizing its role in expanding knowledge and generating new ideas, while Kim focuses on its life-saving applications. Laird argues that research has intrinsic worth by pushing the boundaries of human understanding, which he sees as more valuable than its immediate practical benefits. Kim, however, takes a pragmatic view, emphasizing the direct impact of research on medicine and its capacity to save lives. This fundamental disagreement points to (C), as they differ on whether pure research should prioritize life-saving outcomes over knowledge for knowledge’s sake.",
    ],
    1: [
        "The executive's reasoning infers consumer response to print ads based on the underwhelming response to digital ads in the same campaign. This assumption draws parallels between two advertising mediums within the same context without direct evidence from print media. The reasoning uses the digital response as an analogy to make inferences about print, which makes (D) the most accurate answer. The executive's argument relies on analogous evidence due to the lack of direct information on the print ads’ impact.",
        "The executive’s conclusion is based on limited consumer response to online advertisements, extrapolating that response levels to print ads were likely below par as well. The reasoning here involves inferring from an analogous case, as the executive uses data from one medium (online ads) to predict the results of another (print ads) within the same campaign context. Thus, (D) is the correct answer, highlighting the use of indirect evidence to draw conclusions about a related but unmeasured case.",
    ],
    2: [
        "The Quebec Bridge disaster highlights the limitations of engineering practices that relied on informal 'rules of thumb' before formal guidelines were developed. This suggests that engineers used such rules because rigorous analytical methods or technologies were inadequate at the time. Thus, the correct inference is (C), indicating that reliance on less formalized methods was not necessarily negligent but instead a product of limited engineering resources and analysis available before the incident reformed engineering practices.",
        "The collapse of the Quebec Bridge in 1907 revealed a significant reliance on informal engineering methods. This event, followed by a shift in engineering standards, suggests that engineers previously depended on rules of thumb, likely due to inadequate or less rigorous analytical methods. Therefore, (C) is the best answer, as it reflects the historical reliance on simplified methods that were later deemed insufficient, underscoring the limitations in engineering practices prior to the disaster.",
    ],
    3: [
        "The absence of a neutron star after the 1987 supernova challenges the assumption that such explosions always produce neutron stars. Supporting this argument requires evidence that neutron stars can arise from events other than supernovas, which would make the exception in 1987 plausible. The best answer is (E), as it introduces the idea that alternative causes for neutron star formation exist, reinforcing the claim that the supernova’s unique outcome does not invalidate the general theory but suggests other formation pathways.",
        "The missing neutron star following the 1987 supernova raises questions about the theory that supernovas always result in neutron stars. Evidence that other sources can create neutron stars, as in (E), strengthens the argument by challenging the notion that neutron stars must arise exclusively from supernovas, thereby allowing for variability in post-supernova remnants and supporting the anomalous outcome of the 1987 event.",
    ],
    4: [
        "The political scientist's argument asserts that democracy does not inherently promote freedom, citing examples of democratic oppression and despotisms that allow freedom. This reasoning confuses the concepts of necessary and sufficient conditions for freedom; just because democracy is not a guaranteed path to freedom, it does not mean it cannot promote it. Therefore, the best answer is (A), as the scientist mistakenly equates democracy’s lack of sufficiency for freedom with its complete inability to support freedom.",
        "The political scientist’s reasoning suggests that democracy does not guarantee freedom, using examples of democratic oppression and freedoms within certain despotisms. This logic conflates necessary and sufficient conditions, as democracy’s lack of absolute guarantee for freedom does not imply it is incapable of fostering it under the right conditions. The answer, therefore, is (A), indicating the flaw lies in confusing democracy’s potential for promoting freedom with its necessity or sufficiency in doing so.",
    ],
    5: [
        "The journalist critiques the practice of pharmaceutical companies setting high drug prices in wealthy nations and lower prices in poorer ones, implying that equal access to healthcare should be the priority. This argument relies on a principle that those in need should receive priority consideration regardless of their country’s economic status. The answer is (A), as it aligns with the journalist’s perspective that moral obligations should focus on those in the greatest need, rather than differentiating based on wealth.",
        "The journalist critiques the pharmaceutical pricing model, arguing it is unjust for companies to charge higher prices in wealthier countries and lower prices in poorer ones, hinting at a moral imperative for equitable access. The argument hinges on the principle that those in greater need should receive more consideration, regardless of their country’s wealth. This aligns with (A), as it suggests that moral obligations should prioritize those in need rather than making distinctions based on economic status.",
    ],
    6: [
        "Critics claim that formal poetry is inherently conservative, but the argument counters this by highlighting poets like Molly Peacock and Marilyn Hacker, who are progressive feminists. This suggests an underlying assumption that political progressivism is incompatible with conservative expression, regardless of the poetry’s form. The best answer is (C), as it supports the conclusion that a progressive poet’s formal poetry cannot be deemed politically conservative solely based on form, asserting that political ideology supersedes stylistic choices.",
        "The critics argue that writing formal poetry is inherently conservative, but the argument counters this by citing progressive poets, implying that if poets are politically progressive, their work cannot be considered conservative despite its form. The answer, (C), supports this by assuming that political progressivism is incompatible with conservative acts, which, if true, substantiates the counterargument.",
    ],
    7: [
        "The argument regarding early human ancestor bones found in lake sediments depends on the assumption that these remains predate the lake’s drying. This condition is necessary to validate the claim that early humans lived in the area during the specified period. The best answer is (E), as it substantiates the argument by confirming the timeline required for early human habitation in that region.",
        "The argument concerning human ancestors relies on the assumption that the bones found were deposited in the lake sediments before it dried, which supports the claim about the time frame of early human habitation. Therefore, (E) is the answer, as this assumption is essential to the timeline posited by the argument.",
    ],
    8: [
        "The discrepancy in collision rates between optional and mandatory headlight use can be explained by recognizing that drivers who voluntarily use headlights tend to be more cautious. This difference suggests that careful drivers who use headlights by choice are more likely to avoid collisions, which mandatory rules alone do not ensure. Therefore, (C) resolves the discrepancy by linking voluntary headlight use with cautious driving behavior, a factor not inherently promoted by mandatory headlight use.",
        "The discrepancy between collision rates under optional and mandatory headlight use is resolved by recognizing that careful drivers—who are likely to use headlights voluntarily—are less prone to collisions. Thus, (C) addresses the inconsistency by suggesting that voluntary headlight users tend to be more cautious, which is not guaranteed when headlight use is mandated.",
    ],
    9: [
        "The suggestion that Carpaccio painted “Erato Declaiming” based solely on its use of red echoes flawed reasoning patterns where superficial characteristics are used to attribute authorship without definitive evidence. Here, (D) exhibits similar reasoning by inferring an artwork’s origin based on medium rather than concrete stylistic or historical proof, thus committing the same error of attributing significance to incidental traits rather than substantial evidence.",
        "The inference that “Erato Declaiming” is by Carpaccio due to its use of red parallels reasoning that links an artist’s identity solely to stylistic characteristics. Similarly, (D) contains this flawed reasoning, as it presumes that specific artistic features automatically determine the origin without further substantiation, relying solely on medium association rather than conclusive evidence.",
    ],
}


# For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.

qa_pairs = [{"question": q, "answer": answers[i]} for i, q in enumerate(questions)]

# home page
@app.route("/")
def index():
    theme = session.get('theme', 'light')
    return render_template("index.html", theme=theme)

@app.route('/set_color', methods=['POST'])
def set_color():
    # Get the color from the form and store it in the session
    color = request.form.get('color')
    session['bg_color'] = color
    return redirect(url_for('index'))

@app.route('/toggle-theme')
def toggle_theme():
    # Check current theme; default to 'light' if not set
    current_theme = session.get('theme', 'light')
    
    # Toggle theme
    if current_theme == 'light':
        session['theme'] = 'dark'
    else:
        session['theme'] = 'light'
    
    return redirect(url_for('index'))

# Define a context processor to inject theme into every template
@app.context_processor
def inject_theme():
    # Get the theme from session, default to 'light' if not set
    theme = session.get('theme', 'light')
    return {'theme': theme}

# survey page
@app.route("/survey")
def survey():
    
    # Initialize session index if it doesn't exist
    if 'index' not in session:
        session['index'] = 0  # Start with the first question

    # Get the current index
    idx = session['index']
    
    # Ensure the index is valid
    if idx < len(qa_pairs):
        qa = qa_pairs[idx]
    else:
        qa = {"question": "End of questions", "answer": ""}

    return render_template('survey.html', qa=qa)
    


# Route to handle the "Next" button on survey page
@app.route('/next')
def next_question():
    # Update the index in session
    session['index'] = (session['index'] + 1) % (len(qa_pairs) + 1)  # Loop back to start
    return redirect(url_for('survey'))

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)