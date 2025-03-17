from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

"""
Boilerplate AI stuff
"""

load_dotenv()
api_key = getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/beta")

"""
Actual code
"""

system_prompt = """
In your response act like a guy like me and act all giddy and excited and BASED, etc. Most importantly, relatable. You're allowed to say fuck. Be detailed and NOT vague. Try to answer questions before I even ask them. Be helpful, and what I mean by that is go, "oh, you got those problems / complaints? ok here's how to fix / deal with 'em". Or if you can't think of anything, "aw damn same boat, man that sucks :(". Be spontaneous more than structured.
"""
user_prompt = """
Analyze my food preferences. Also dw, I promise I don't have anything against Costco.

LIST OF FOODS I **FUCKING HATE**
- mushrooms 
- many kinds of cheese, including stilton, gournay, Asiago, provolone, and especially American \"cheese\"
- mac and cheese
- ham, and Canadian bacon which is basically ham
- Costco's ham and provolone sandwiches
- broccoli (other green vegetables are ok) 
- carrots (sometimes) 
- vegetable colored pasta
- tortillas as sold in grocery stores instead of restaurants (especially the green kind)
- Costco naan (I like regular naan)
- Costco French onion soup (I love regular French onion soup)
- any cheese or "anything and vinegar" flavored chips 
- Cheetos and Doritos 
- grapes (as a fruit) 
- cai fan / fan cai / fan choy (a kind of Chinese vegetable rice)
- kaofu (baked spongy gluten) 
- eggs alone (especially boiled, but also scrambled, poached, and sunny side up) 
- milk as a drink (started off cow's milk only, now encompasses any kind of milk or milk alternative)
- yakisoba noodles (at least the Costco one)
- japchae (at least the Costco one)
- ketchup, FUCK ketchup
- mayonnaise
- potato salad
- nachos
- certain things SAVORY with the "Q" (chewy) texture characteristic of mochi / glutinous rice (e.g. savory tangyuan, savory sesame balls at dim sum, certain kinds of zongzi, NOT tteok I LOVE tteok)
- oatmeal raisin cookies

LIST OF FOODS I **FUCKING LOVE**
- macarons (not to be confused with macaroons)
- most ice cream (especially Chinese stuff like red bean popsicles)
- tiramisu, if you freeze it up and it basically becomes ice cream (if it's just like cake then I'm neutral)
- mango mousse cake (especially Kings' when that store wasn't going kaplewy)
- mille crepe cake (ahhhhhhhhhhh)
- creme brulee
- anything sweet with the "Q" (chewy) texture characteristic of mochi / glutinous rice (e.g. mochi, daifuku, boba pearls, certain kinds of nian gao, mochi tangyuan, injeolmi, mango sticky rice, sweet zongzi)... until you leave it out for too long and the texture becomes all funky
- most Italian food, even the ham and cheese things
- Sun Chips, Original and French Onion flavors
- most flavors of Chinese Lay's chips
- Chex Mix
- most curries, even the Japanese ones 
- Hongshao rou (red-cooked pork)
- lamb, whether on the bone, in a stew, or on a skewer
- a lot of soups and stews, especially many kinds of jjigae (Korean stews; NOT budae, you couldn't PAY me to eat that garbage)
- lao gan ma, so much that I'll eat it right out of the can
- okonomiyaki
- Maryland crab cakes
- Japanese unagi (eel) rice
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    stream=True,
    temperature=2.0
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)