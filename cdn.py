import os
import json
import shutil
import re
import time
from deep_translator import GoogleTranslator

SOURCE_DIR = 'items'
OUTPUT_DIR = 'dist'
API_DIR = os.path.join(OUTPUT_DIR, 'api')
SUPPORTED_LANGS = ['pt', 'es', 'en']
TRANSLATIONS_FILE = 'translations.json'

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def load_translations():
    if os.path.exists(TRANSLATIONS_FILE):
        try:
            with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar translations.json: {e}")
            
    return {lang: {} for lang in SUPPORTED_LANGS}

def save_translations(translations):
    try:
        with open(TRANSLATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar translations.json: {e}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    if not os.path.exists(API_DIR):
        os.makedirs(API_DIR)

    translations = load_translations()
    if not os.path.exists(SOURCE_DIR):
        print(f"Pasta de origem '{SOURCE_DIR}' não encontrada!")
        return

    images = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith('.png')]
    api_data = {}
    
    changed = False

    for lang in SUPPORTED_LANGS:
        lang_dir = os.path.join(OUTPUT_DIR, lang)
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            
        if lang not in translations:
            translations[lang] = {}

    for img in images:
        name_without_ext = os.path.splitext(img)[0]
        api_data[name_without_ext] = {"original": img, "translations": {}}
        
        clean_name = re.sub(r'([A-Z])', r' \1', name_without_ext).replace('_', ' ').replace('-', ' ').strip()
        
        for lang in SUPPORTED_LANGS:
            if name_without_ext not in translations[lang]:
                try:
                    print(f"Traduzindo '{clean_name}' para {lang}...")
                    time.sleep(0.5)
                    translated = GoogleTranslator(source='auto', target=lang).translate(clean_name)
                    if translated:
                        translations[lang][name_without_ext] = translated
                        changed = True
                    else:
                        translations[lang][name_without_ext] = clean_name
                except Exception as e:
                    print(f"Erro ao traduzir '{clean_name}': {e}")
                    translations[lang][name_without_ext] = clean_name
            
            translated_name = translations[lang].get(name_without_ext, clean_name)
            slug = slugify(translated_name)
            if not slug:
                slug = slugify(name_without_ext)
            
            api_data[name_without_ext]["translations"][lang] = f"{slug}.png"
            
            src_path = os.path.join(SOURCE_DIR, img)
            dst_path = os.path.join(OUTPUT_DIR, lang, f"{slug}.png")
            shutil.copyfile(src_path, dst_path)

    original_dist = os.path.join(OUTPUT_DIR, 'original')
    if os.path.exists(original_dist):
        shutil.rmtree(original_dist)
    shutil.copytree(SOURCE_DIR, original_dist)
            
    if changed:
        save_translations(translations)
        
    with open(os.path.join(API_DIR, 'search.json'), 'w', encoding='utf-8') as f:
        json.dump(api_data, f, ensure_ascii=False, indent=2)

    print("Build da CDN Concluído! Copias de imagens e traduções foram geradas com sucesso.")

if __name__ == "__main__":
    main()
