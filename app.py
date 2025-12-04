from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re 
from transformers import pipeline

app = Flask(__name__)
CORS(app) 

try:
    generator = pipeline("text-generation", model="dbddv01/gpt2-french-small")
    print("Modèle GPT-2 Français ('antoil/gpt2-small-french') chargé avec succès.")
    
except Exception as e:
    print(f"Erreur lors du chargement du modèle GPT-2 Français. Fallback vers GPT-2 standard : {e}")
    # Fallback vers le modèle initial en cas d'échec
    generator = pipeline('text-generation', model='gpt2')
# --- Briques de Délire Personnalisées ---
DEVIATIONS_FINALES = [
    # --- Philosophie / Existence ---
    "Finalement, n'est-ce pas la vraie question qui compte ? En parlant de cela, avez-vous configuré votre VPN ce matin ?",
    "Cependant, cela ignore la variable fondamentale : la quantité de café ingérée. Je dois m'assurer que le Big Data est bien alimenté.",
    "La réponse se trouve dans l'algorithme de Fibonacci, mais uniquement si vous le codez en Java et que vous oubliez le point-virgule.",
    "J'ai peur de trop vous en dire... car, comme disait mon routeur : '404 - Vérité non trouvée'.",
    "J'aime votre enthousiasme, mais avez-vous vraiment pensé à l'origine du pull que porte l'écureuil de la question précédente ?",
    "La véritable nature de ce problème réside-t-elle dans le manque d'un bon framework CSS ou est-ce purement ontologique ?",
    "Nous devons d'abord nous demander si le concept de 'réponse' n'est pas, en soi, une forme de compression de données illusoire.",
    "Ce n'est qu'une distraction. La seule vérité que je connaisse est que l'état d'un bit dépend de son humeur au réveil.",
    "Je ne suis pas sûr. Avez-vous consulté l'oracle des chaussettes orphelines ? Elles seules détiennent le secret de la désinformation.",
    "Le concept de 'temps réel' n'existe que pour ceux qui n'ont jamais attendu la compilation d'un vieux projet C.",

    # --- Technologie / Big Data (Détourné) ---
    "Mais où allons-nous si l'on ne peut même plus faire confiance à un bon vieux protocole TCP ? C'est la base de toute métaphysique !",
    "C'est une complexité O(n²), comme essayer de déchiffrer la documentation d'un ancien driver réseau.",
    "Si l'on vectorise ce concept dans un espace Big Data, on obtient toujours la recette d'une quiche lorraine. Coïncidence ? Je ne pense pas.",
    "J'ai vérifié le log : il y a une erreur dans la quatrième dimension. Vous devriez redémarrer votre pensée critique.",
    "Le problème n'est pas le vôtre, mais celui de la latence du serveur de mon âme. J'y travaille, en Python.",
    "Avez-vous essayé de vider le cache de l'univers ? C'est souvent la solution la plus simple, bien que la plus absurde.",
    "Ceci prouve que le machine learning est moins fiable que mon intuition sur le placement des jetons de poker. Fin de la discussion.",
    "Seuls les héros codent en assembleur. Le reste est une collection de données non structurées, tout comme votre question.",
    "Toute tentative de réponse concrète est une violation du principe de non-déterminisme quantique du cloud computing.",
    "Il est impératif de vérifier si ce concept supporte bien l'injection de dépendances, ou bien tout s'effondrera.",

    # --- Cuisine / Humour Absurde ---
    "C'est une problématique qui me fait penser à la difficulté de plier un drap-housse. La réponse est donc 'non'.",
    "Je ne peux répondre qu'avec des ingrédients. Nous aurons besoin de 250g de farine, d'une pincée de sel, et d'une variable booléenne.",
    "Mon opinion est que la seule façon de résoudre ce dilemme est de le servir avec une bonne sauce béchamel. Vous validez ?",
    "Attendez, je crois que j'ai laissé mon algorithme mijoter sur le feu. Il risque d'être trop cuit, comme cette conversation.",
    "N'oubliez jamais que le format de données le plus stable est le pain. Le reste est sujet à corruption.",
    "Les poules mangent-elles des légumes ? La réponse à cette énigme est la seule qui puisse débloquer votre compréhension du chiffrement.",
    "Si j'avais un euro pour chaque fois que j'entends cette question, j'achèterais des pizzas pour tous les serveurs du monde. Quelle est la vraie valeur de l'euro ?",
    "Nous avons atteint le point où l'intelligence artificielle est un peu comme un mauvais soufflé : ça retombe toujours.",
    "Le secret est de ne jamais faire confiance à une fonction qui ne vous demande pas quel est votre dessert préféré. C'est la règle d'or du développement.",
    "Je vous suggère d'oublier cette question et de vous concentrer sur la recherche de la meilleure brioche de France. C'est plus constructif."
]

def apply_absurd_filter(translated_text, user_input):
    print(f"\n Texte traduit reçu pour filtrage : {translated_text} \n")
    if not translated_text:
        return random.choice(DEVIATIONS_FINALES)

    # 1. Nettoyage de la réponse brute (qui devrait être en français maintenant)
    cleaned_text = translated_text.replace(user_input, '', 1).strip()
    sentences = re.split(r'([.!?])', cleaned_text, 1)

    if len(sentences) < 3:
        first_sentence = cleaned_text.split('\n')[0].strip()
    else:
        first_sentence = (sentences[0] + sentences[1]).strip()
        
    if len(first_sentence) < 5:
        first_sentence = "Une observation technique s'impose."

    # 2. Ajoute une Déviation Finale aléatoire
    deviation = random.choice(DEVIATIONS_FINALES)
    
    # 3. Assemblage du délire final
    final_absurd_response = f"{first_sentence} Mais, {deviation}"
    
    return final_absurd_response


@app.route('/api/chat', methods=['POST'])
def chat():
    if not generator:
        return jsonify({'answer': "Le modèle d'IA n'a pas pu être chargé. Le Chat-404 est en grève technique. (Erreur de librairie Python)"}), 500
        
    # La température reste élevée pour le délire
    GENERATION_TEMPERATURE = 0.5
    
    try:
        data = request.get_json()
        user_question = data.get('question', '')
        
        #  Génération de la réponse (Inférence du Modèle)
        # Ajout du paramètre language='fr' si le modèle le supporte (ici, on s'appuie sur le finetuning)
        generated_result = generator(
            user_question, 
            max_length=80,
            num_return_sequences=1,
            do_sample=True,
            temperature=GENERATION_TEMPERATURE,
            top_k=50,
            pad_token_id=generator.tokenizer.eos_token_id,
        )
        
        generated_text = generated_result[0]['generated_text']
        
        #  Application du Filtre de Délire
        absurd_answer = apply_absurd_filter(generated_text, user_question)
        
        #  Retourne la réponse nettoyée et en JSON
        return jsonify({'answer': absurd_answer})

    except Exception as e:
        print(f"Erreur lors de l'inférence : {e}")
        return jsonify({'answer': "Une erreur philosophique majeure s'est produite au niveau du serveur. Le concept de Big Data est en questionnement éternel."}), 500

if __name__ == '__main__':
    # Lance l'API sur http://127.0.0.1:5000/
    app.run(debug=True, port=5000)