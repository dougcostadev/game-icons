# Game Icons CDN

CDN de Imagens Grátis rodando 100% via GitHub Pages com rotas API-like traduzidas.

## Arquitetura
Sempre que você commita uma nova imagem na pasta `items/` na branch `main`, o **GitHub Actions** executa o script `build_cdn.py`.
Este script processará as imagens `*.png`, fará a **tradução automática do nome delas** (usando um cache salvo em `translations.json` para ficar super rápido na próxima vez), e criará cópias nas pastas traduzidas correspondentes (`pt/`, `es/`, `en/`). Estas cópias são então exportadas para o **GitHub Pages**, criando uma CDN gratuita para as imagens e tornando viável as URLs API-like sem precisar de backend!

Exemplos de Uso após o Deploy:
```html
<!-- Exibir uma imagem traduzida diretamente -->
<img src="https://dougcostadev.github.io/game-icons/pt/espada.png" />
<img src="https://dougcostadev.github.io/game-icons/en/sword.png" />
```

E para listar tudo de forma dinâmica se precisar, basta buscar o JSON da API gerado estaticamente pelo script:
```js
fetch('https://dougcostadev.github.io/game-icons/api/search.json')
  .then(res => res.json())
  .then(data => console.log(data));
```

## Passo a Passo para Ativar a CDN:

1. Suba todo esse código para o seu repositório GitHub e dê Push (Push na branch `main`).
2. Acesse seu repositório no GitHub e vá em **Settings -> Pages**
3. Em **Build and deployment -> Source**, selecione a opção **GitHub Actions**.
4. É só isso! Nas próximas vezes que você alterar o repositório, clique na aba **Actions** para assistir o seu site sendo feito, publicando os links de cada idioma traduzido no seu site `.github.io`!