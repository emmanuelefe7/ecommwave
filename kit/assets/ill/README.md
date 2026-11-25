Illustrations from unDraw (undraw.co, free for commercial use, no attribution required), via the npm package `undraw-svg`.
Recolored to the brand: accent (currentColor) -> #12b886, dark ink -> navy #152a59 / #1f3a78.
More: `npm pack undraw-svg` (1,700+ scenes in package/svgs/), recolor with the same sed:
  sed -e 's/currentColor/#12b886/g' -e 's/#090814/#152a59/gi' -e 's/#2f2e41/#152a59/gi' -e 's/#3f3d56/#1f3a78/gi'
Never use scenes showing real brand logos (e.g. social-growth has social network logos).
