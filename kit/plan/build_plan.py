import json, datetime
D0 = datetime.date(2026, 11, 29)
H = {  # hashtag sets (exactly 5)
 'email': '#EmailMarketing #ShopifyTips #EcommerceMarketing #RepeatCustomers #ShopifyStore',
 'trust': '#ShopifyTips #OnlineStoreTips #EcommerceTips #ShopifyStore #SmallBusinessTips',
 'cro': '#ShopifyTips #ConversionRateOptimization #EcommerceGrowth #OnlineStoreTips #ShopifyExpert',
 'design': '#ShopifyDesign #ShopifyTips #EcommerceTips #WebDesignTips #ShopifyStore',
 'seo': '#ShopifySEO #EcommerceSEO #ShopifyTips #OnlineStoreTips #SmallBusinessTips',
 'holiday': '#HolidaySales #ShopifyTips #EcommerceMarketing #ChristmasShopping #ShopifyStore',
 'ads': '#FacebookAds #EcommerceMarketing #ShopifyTips #DTCBrand #EcommerceGrowth',
 'social': '#InstagramForBusiness #ShopifyTips #UGC #EcommerceMarketing #SmallBusinessTips',
 'photo': '#ProductPhotography #ShopifyTips #EcommerceTips #ShopifyDesign #OnlineStoreTips',
 'growth': '#EcommerceGrowth #ShopifyTips #ShopifyExpert #DTCBrand #BrandBuilding',
}
# (row, slot, format, look, topic, hook, opener, keywords, tags, trigger)
T = {}
def add(day, row, slot, fmt, look, topic, hook, opener, kw, tags, trig):
    T.setdefault(day, []).append(dict(day=day, row=row, slot=slot, format=fmt, look=look, topic=topic, hook=hook,
         opener=opener, keywords=kw, hashtags=H[tags], trigger=trig))
S, SV = 'Send this to a store owner who needs it', 'Save this for your next store update'
# ---------- Day 1 (Sun Nov 29, Cyber Monday eve) ----------
add(1,'L-N-L','LEFT','Carousel','LIGHT','Cyber Monday sale email in 4 parts: subject, preview line, first image, one button',
    'Your Cyber Monday email gets ignored? Fix 4 parts.','Cover: inbox UI with your email buried between 9 others',
    'cyber monday email, sale email subject lines, shopify email','email',SV)
add(1,'L-N-L','MIDDLE','Reel','NAVY','Show real stock levels honestly ("Only 3 left" only when true) instead of hiding stock',
    'Customers think it will always be there?','0–2s: big "Only 3 left" chip pops on a NOVA product page + voice "Is this real?"',
    'low stock message, shopify inventory, urgency without fake timers','cro',S)
add(1,'L-N-L','RIGHT','Single','LIGHT','Checklist before you hit send on a sale email (link works, code works, ends date, phone preview)',
    'About to send your sale email? Check these first.','Headline over a realistic phone email preview with 4 check chips',
    'sale email checklist, email marketing tips, shopify email','email',SV)
add(1,'SIMILAR-3','RIGHT','Single','NAVY','Instagram post that sells #3: behind the scenes (packing orders, making the product)',
    'Customers follow people, not logos. Show behind the scenes.','Tile: real packing-table photo card + one headline',
    'instagram for shopify, behind the scenes content, small business instagram','social',S)
add(1,'SIMILAR-3','MIDDLE','Single','NAVY','Instagram post that sells #2: a customer photo with their words',
    'Your best ad is a customer photo.','Tile: phone with a customer photo post + quote line',
    'user generated content, customer photos, instagram shopping','social',S)
add(1,'SIMILAR-3','LEFT','Single','NAVY','Instagram post that sells #1: the product in use, not on white',
    'Posting product photos nobody stops for?','Tile: same product on white vs in use, one arrow',
    'product in use photos, instagram product posts, shopify marketing','social',S)
add(1,'N-L-N','RIGHT','Reel','NAVY','Mistake: product photos that don\'t match (mixed backgrounds, sizes, lighting) make the store look cheap',
    'Your product photos make your store look cheap.','0–2s: collection grid snaps from messy to matching on the word "cheap"',
    'product photo consistency, shopify collection page, ecommerce product photos','photo',S)
add(1,'N-L-N','MIDDLE','Single','LIGHT','A shipping page customers trust: delivery times, costs, countries, what happens if it\'s late',
    'Customers leave to look for your shipping info?','Headline + realistic shipping page UI with 4 clear rows',
    'shipping policy page, shopify shipping page, delivery times','trust',SV)
add(1,'N-L-N','LEFT','Reel','NAVY','Growth: a packaging insert card that brings the second order (thank you, how to use, next-order reason)',
    'Your box can sell the next order.','0–2s: box opens, card slides out with "Thanks, Sam!"',
    'packaging insert card, repeat customers, unboxing experience','growth',S)
add(1,'CONNECTED-6','1-6','6 singles','NAVY','6 ways a first-time visitor decides to trust your store (real photos, reviews, contact, policies, secure checkout, about you)',
    'Would a stranger trust your store in 5 seconds?','Tile 1 hook; tiles 2–6 one trust fix each; tile 6 free audit CTA',
    'store trust signals, new shopify store, build customer trust','trust',S)
# ---------- Day 2 (Mon Nov 30, Cyber Monday) ----------
add(2,'L-N-L','LEFT','Carousel','LIGHT','Build a holiday gift guide page: by price, by person, ships-by date, gift cards at the end',
    'Shoppers can\'t decide what to gift? Build this page.','Cover: realistic gift guide page with "Under $25 / $50 / $100" tabs',
    'holiday gift guide, shopify gift guide page, christmas gift ideas page','holiday',SV)
add(2,'L-N-L','MIDDLE','Reel','NAVY','Browse-abandonment email: they looked, didn\'t add to cart; send one helpful reminder',
    'They looked. They left. No cart. Now what?','0–2s: product page view → phone locks → email notification lands',
    'browse abandonment email, klaviyo flows, shopify email automation','email',S)
add(2,'L-N-L','RIGHT','Single','LIGHT','Gift message and "hide prices on packing slip" options at checkout',
    'Buying a gift? Let them hide the price.','Headline + checkout UI with gift note box and toggle',
    'gift message checkout, shopify gift options, holiday checkout','holiday',S)
add(2,'SIMILAR-3','RIGHT','Single','LIGHT','Checkout trust line #3: delivery date right above the Pay button',
    'Show when it arrives, right above Pay.','Tile: checkout UI, mint highlight on "Arrives Thu, Dec 10"',
    'checkout delivery date, shopify checkout tips, reduce checkout abandonment','cro',SV)
add(2,'SIMILAR-3','MIDDLE','Single','LIGHT','Checkout trust line #2: returns promise in one short line',
    'Worried customers don\'t pay. Add one line.','Tile: checkout UI, "Free 30-day returns" line highlighted',
    'returns policy checkout, shopify checkout trust, cart abandonment','cro',SV)
add(2,'SIMILAR-3','LEFT','Single','LIGHT','Checkout trust line #1: secure checkout + the payment methods they know',
    'Customers stop at checkout? Show it\'s safe.','Tile: checkout UI, padlock line + payment row',
    'secure checkout, shopify payments, checkout trust badges','cro',SV)
add(2,'N-L-N','RIGHT','Reel','NAVY','Mistake: no delivery estimate on the product page ("When will it arrive?")',
    '"When will it arrive?" Your page doesn\'t say.','0–2s: customer taps around the page, question mark scribble, no answer',
    'delivery estimate product page, shopify shipping times, holiday delivery','cro',S)
add(2,'N-L-N','MIDDLE','Single','LIGHT','Set holiday reply times: say when you answer messages and stick to it',
    'Customers messaging you over the holidays?','Headline + chat widget UI "We reply within 4 hours, 9–6"',
    'customer service holidays, live chat shopify, reply time','trust',SV)
add(2,'N-L-N','LEFT','Reel','NAVY','Growth: a "how to use it" email after delivery (fewer returns, more reviews)',
    'Delivered isn\'t done. Send this email next.','0–2s: "Delivered" notification → email "Getting started with your…" slides in',
    'post purchase email, how to use email, shopify email flows','email',S)
add(2,'CONNECTED-6','1-6','6 singles','LIGHT','6 email flows every store should run (welcome, cart, browse, thank you, how-to-use, win-back)',
    'Still sending every email by hand?','Each tile = one flow with a realistic email UI; tile 6 CTA',
    'email flows shopify, email automation, klaviyo flows ecommerce','email',SV)
# ---------- Day 3 (Tue Dec 1, Giving Tuesday) ----------
add(3,'L-N-L','LEFT','Carousel','LIGHT','Google Shopping basics: free product listings for Shopify stores (feed, titles, photos, prices match)',
    'Your products could show on Google. For free.','Cover: realistic Google-style shopping row with NOVA products (no Google logo)',
    'google shopping shopify, free product listings, google merchant center','seo',SV)
add(3,'L-N-L','MIDDLE','Reel','NAVY','Product comparison table: help customers pick between similar products',
    '"Which one should I buy?" Answer it for them.','0–2s: two similar products side by side, "?" bouncing between them',
    'product comparison table, help customers choose, shopify product page','cro',S)
add(3,'L-N-L','RIGHT','Single','LIGHT','Product care guide on the page and in the box (builds trust, fewer returns)',
    'Show customers how to care for it.','Headline + product page "Care" tab UI with 3 icons',
    'product care guide, reduce returns, product page tabs','trust',SV)
add(3,'SIMILAR-3','RIGHT','Single','NAVY','Email after delivery #3: easy reorder button for things that run out',
    'Running low? Let them reorder in one tap.','Tile: email UI with one big "Reorder" button',
    'reorder email, replenishment email, repeat purchase','email',S)
add(3,'SIMILAR-3','MIDDLE','Single','NAVY','Email after delivery #2: ask for a review once it\'s been used',
    'Ask for the review when they\'ve used it.','Tile: email UI with tap-a-star row',
    'review request email, get more reviews, shopify reviews','email',S)
add(3,'SIMILAR-3','LEFT','Single','NAVY','Email after delivery #1: "here\'s how to use it" tips',
    'It arrived. Now help them love it.','Tile: email UI with 3 short tips + product photo',
    'post purchase email, customer onboarding email, ecommerce email','email',S)
add(3,'N-L-N','RIGHT','Reel','NAVY','Mistake: leftover theme demo text ("Your headline here", "Lorem ipsum", "Welcome to our store")',
    'Your store still says "Your headline here"?','0–2s: zoom into a footer that says "Lorem ipsum", red circle',
    'shopify theme setup, store launch checklist, shopify mistakes','design',S)
add(3,'N-L-N','MIDDLE','Single','LIGHT','Write email subject lines that get opened (clear, specific, personal, no ALL CAPS)',
    'Your emails don\'t get opened? Start with the subject.','Headline + inbox UI: weak vs clear subject lines',
    'email subject lines, email open rate, ecommerce email tips','email',SV)
add(3,'N-L-N','LEFT','Reel','NAVY','Growth: a product finder quiz ("Find your perfect…") for stores with many options',
    'Too many products? Let a quiz choose.','0–2s: 3 quick quiz taps → "Your match" product card',
    'product quiz shopify, product finder, help customers choose','growth',S)
add(3,'CONNECTED-6','1-6','6 singles','NAVY','6 product page details customers look for before they buy (size, delivery date, returns, reviews, real photos, what\'s in the box)',
    'Your product page is missing what customers look for.','Each tile = one detail on a realistic NOVA phone; tile 6 CTA',
    'product page checklist, shopify product page, product page conversion','cro',SV)
# ---------- Day 4 (Wed Dec 2) ----------
add(4,'L-N-L','LEFT','Carousel','LIGHT','Work with micro creators: send product, ask for an honest video, get permission to reuse it',
    'Need content but can\'t pay influencers?','Cover: phone with a creator-style video frame + "Gifted" chip',
    'micro influencers, influencer seeding, ugc for shopify','social',SV)
add(4,'L-N-L','MIDDLE','Reel','NAVY','Order tracking page that sells: status first, then "while you wait" products',
    'Customers check tracking 5 times. Use that page.','0–2s: tracking bar fills "Shipped → Out for delivery", products slide in below',
    'order tracking page, shopify order status, post purchase upsell','growth',S)
add(4,'L-N-L','RIGHT','Single','LIGHT','Exit-intent offer that isn\'t a discount (gift guide, free shipping reminder, save your cart)',
    'Leaving popup? Don\'t just throw 10% off.','Headline + popup UI "Save your cart for later"',
    'exit intent popup, cart abandonment, shopify popup tips','cro',S)
add(4,'SIMILAR-3','RIGHT','Single','LIGHT','Product photo shot #3: close-up of the material/detail',
    'Customers can\'t touch it. Show the detail.','Tile: zoomed detail photo inside a product gallery UI',
    'product photography tips, detail shots, ecommerce photos','photo',SV)
add(4,'SIMILAR-3','MIDDLE','Single','LIGHT','Product photo shot #2: the product in someone\'s hand / in use',
    'Show it being used, not just sitting there.','Tile: in-use photo in gallery UI',
    'lifestyle product photos, product in use, shopify product images','photo',SV)
add(4,'SIMILAR-3','LEFT','Single','LIGHT','Product photo shot #1: show the real size (next to something familiar)',
    '"It looked bigger online." Show the real size.','Tile: photo with size reference + measurement chip',
    'product size photo, reduce returns, product photography','photo',SV)
add(4,'N-L-N','RIGHT','Reel','NAVY','Mistake: random trust badges ("100% guaranteed", fake seals) that don\'t mean anything',
    'Those trust badges might be hurting you.','0–2s: page full of badges, they shake and fall off on "hurting"',
    'trust badges shopify, real trust signals, ecommerce credibility','trust',S)
add(4,'N-L-N','MIDDLE','Single','LIGHT','Image SEO: name photo files and write alt text so Google can find your products',
    'Your product photos are invisible to Google.','Headline + file-name before/after chips + alt text field UI',
    'image seo shopify, alt text products, shopify seo tips','seo',SV)
add(4,'N-L-N','LEFT','Reel','NAVY','Growth: replenishment reminder email ("Running low?") for products that run out',
    'They\'ll run out. Remind them first.','0–2s: bottle level drains on the product photo, email pops',
    'replenishment email, subscription alternative, repeat orders','email',S)
add(4,'CONNECTED-6','1-6','6 singles','LIGHT','6 ways to get more reviews (ask after use, one tap stars, photo option, reply to every review, show them high, thank reviewers)',
    'Customers love your product but never review it?','Each tile one tactic with realistic review UI; tile 6 CTA',
    'get more reviews, product reviews shopify, review request','trust',S)
# ---------- Day 5 (Thu Dec 3) ----------
add(5,'L-N-L','LEFT','Carousel','LIGHT','Audit your Shopify apps: list, check what each does, delete unused, check speed after',
    'Paying for apps that slow your store down?','Cover: realistic app list with 3 "unused" red chips',
    'shopify apps, store speed, shopify app audit','cro',SV)
add(5,'L-N-L','MIDDLE','Reel','NAVY','A guarantee that removes the risk (say what you promise in plain words, near the button)',
    'Customers scared to try? Take the risk away.','0–2s: hand hovers over Add to cart, hesitates; guarantee line appears',
    'money back guarantee, reduce purchase risk, shopify conversion','cro',S)
add(5,'L-N-L','RIGHT','Single','LIGHT','Wording for a handwritten-style thank-you card in the box',
    'One small card. A customer for life.','Headline + real-looking card with short message',
    'thank you card small business, packaging ideas, customer loyalty','growth',S)
add(5,'SIMILAR-3','RIGHT','Single','NAVY','Question to ask customers #3: "How did you hear about us?" (post-purchase)',
    'Not sure which marketing works? Ask customers.','Tile: thank-you page survey UI',
    'post purchase survey, marketing attribution, customer feedback','growth',S)
add(5,'SIMILAR-3','MIDDLE','Single','NAVY','Question to ask customers #2: "What almost stopped you from buying?"',
    'Ask this. Fix what they tell you.','Tile: survey answer chips (shipping, size, price…)',
    'customer survey questions, conversion insights, shopify feedback','growth',S)
add(5,'SIMILAR-3','LEFT','Single','NAVY','Question to ask customers #1: "Why did you buy?" (use their words in your copy)',
    'Your customers will write your ads for you.','Tile: survey reply card → highlighted words',
    'customer research, voice of customer, product copywriting','growth',S)
add(5,'N-L-N','RIGHT','Reel','NAVY','Mistake: making phone number required at checkout without saying why',
    'Phone number required? Customers think "spam".','0–2s: required field shakes red, cursor hesitates',
    'checkout fields, shopify checkout settings, checkout abandonment','cro',S)
add(5,'N-L-N','MIDDLE','Single','LIGHT','Product page meta title & description: write what shows on Google',
    'What does Google show for your products?','Headline + search-result style card (no Google logo) before/after',
    'meta description shopify, product seo, shopify seo title','seo',SV)
add(5,'N-L-N','LEFT','Reel','NAVY','Growth: show "Recently viewed" products on every page',
    'Customers lose what they looked at. Show it again.','0–2s: customer scrolls away, "Recently viewed" row slides up',
    'recently viewed products, shopify product recommendations, browse to buy','cro',S)
add(5,'CONNECTED-6','1-6','6 singles','NAVY','6 fixes for a slow store on phones (smaller photos, fewer apps, no autoplay video, fewer fonts, one popup, lighter theme)',
    'Customers leave before your page even loads?','Each tile one speed fix with phone UI; tile 6 CTA',
    'shopify speed optimization, mobile site speed, slow shopify store','cro',SV)
# ---------- Day 6 (Fri Dec 4) ----------
add(6,'L-N-L','LEFT','Carousel','LIGHT','Get customer videos (UGC): when to ask, what to ask, make it easy, say thank you',
    'Want real customer videos? Here\'s how to ask.','Cover: phone frame of a customer-style video + "Shared by Maya"',
    'ugc content, customer videos, user generated content ecommerce','social',SV)
add(6,'L-N-L','MIDDLE','Carousel','NAVY','Good-better-best: offer 3 clear choices (single, pair, set) honestly priced',
    'Only one option? Give customers three.','Cover: three product cards, middle one "Most chosen"',
    'product bundles pricing, good better best, average order value','cro',SV)
add(6,'L-N-L','RIGHT','Single','LIGHT','Returns email that keeps the customer: offer an exchange first, kindly',
    'A return doesn\'t have to lose the customer.','Headline + email UI "Want a different size instead?"',
    'returns email, exchange instead of refund, customer retention','email',S)
add(6,'SIMILAR-3','RIGHT','Single','LIGHT','Weekly number #3: orders and what each customer spends (average order value, in plain words)',
    'Check this number every Monday.','Tile: clean stat card (example label) + one line',
    'shopify analytics, average order value, ecommerce kpis','growth',SV)
add(6,'SIMILAR-3','MIDDLE','Single','LIGHT','Weekly number #2: how many visitors add to cart',
    'Visitors, but no carts? This number tells you.','Tile: stat card "Added to cart" (example)',
    'add to cart rate, shopify reports, conversion rate','growth',SV)
add(6,'SIMILAR-3','LEFT','Single','LIGHT','Weekly number #1: where your visitors come from',
    'Do you know where your visitors come from?','Tile: traffic source card (example) with 3 rows',
    'shopify traffic sources, ecommerce analytics, marketing channels','growth',SV)
add(6,'N-L-N','RIGHT','Reel','NAVY','Mistake: social icons that lead to empty or old accounts',
    'Your Instagram link shows posts from 2023?','0–2s: tap footer icon → empty profile slides in',
    'social proof, small business instagram, store credibility','trust',S)
add(6,'N-L-N','MIDDLE','Single','LIGHT','An FAQ page that sells: answer shipping, returns, sizing, payment, contact',
    'Customers keep asking the same questions?','Headline + FAQ accordion UI with 5 rows',
    'faq page shopify, ecommerce faq, customer questions','trust',SV)
add(6,'N-L-N','LEFT','Reel','NAVY','Growth: a short founder video on the About and product pages',
    'Customers buy from people. Show your face.','0–2s: play button on a founder frame, "Hi, I\'m…" caption',
    'founder story video, about us page, brand trust','growth',S)
add(6,'CONNECTED-6','1-6','6 singles','LIGHT','6 last-week holiday fixes (ship-by date, gift cards, gift notes, holiday returns, reply times, best sellers first)',
    'One week left for holiday orders. Fix these.','Each tile one fix with realistic UI; tile 6 CTA',
    'holiday ecommerce checklist, christmas shipping deadline, holiday sales tips','holiday',SV)
# ---------- Day 7 (Sat Dec 5) ----------
add(7,'L-N-L','LEFT','Carousel','LIGHT','Collection page SEO: a short intro text, clear names, filters, internal links',
    'Your collection pages could rank on Google.','Cover: collection page UI with highlighted intro text',
    'collection page seo, shopify seo, category page optimization','seo',SV)
add(7,'L-N-L','MIDDLE','Reel','NAVY','Pre-orders for sold-out best sellers (say the ship date clearly)',
    'Sold out? Keep selling with pre-orders.','0–2s: "Sold out" stamp flips to "Pre-order · ships Jan 12"',
    'pre order shopify, sold out products, inventory planning','growth',S)
add(7,'L-N-L','RIGHT','Single','LIGHT','Late order email: say sorry first, give the new date, offer a small thank-you',
    'Order running late? Send this before they ask.','Headline + email UI with apology + new date',
    'late delivery email, customer service email, order delay','email',S)
add(7,'SIMILAR-3','RIGHT','Single','NAVY','Sign your ads won\'t pay off #3: no reviews on the page the ad opens',
    'Ads won\'t work on a page with no reviews.','Tile: ad card → product page with empty stars',
    'facebook ads shopify, ad landing page, ads not converting','ads',S)
add(7,'SIMILAR-3','MIDDLE','Single','NAVY','Sign your ads won\'t pay off #2: the page loads slowly on phones',
    'Slow page? Your ad money leaks out.','Tile: ad card → loading spinner phone',
    'ads not converting, mobile page speed, ad spend wasted','ads',S)
add(7,'SIMILAR-3','LEFT','Single','NAVY','Sign your ads won\'t pay off #1: the page doesn\'t match the ad',
    'Ad says one thing, page shows another?','Tile: ad card with red dress → page with something else',
    'ad landing page match, facebook ads tips, shopify ads','ads',S)
add(7,'N-L-N','RIGHT','Reel','NAVY','Mistake: an expired sale banner still up ("Black Friday ends Sunday" in December)',
    'Your Black Friday banner is still up?','0–2s: calendar flips to December, old banner flashes red',
    'sale banner, store maintenance, shopify announcement bar','design',S)
add(7,'N-L-N','MIDDLE','Single','LIGHT','Saved replies for customer service (where is my order, change address, returns, sizing)',
    'Typing the same reply 20 times a day?','Headline + inbox UI with 4 saved reply chips',
    'customer service templates, saved replies, shopify inbox','trust',SV)
add(7,'N-L-N','LEFT','Reel','NAVY','Growth: use customers\' own words (from reviews) in your product copy',
    'Your customers already wrote your best copy.','0–2s: review highlight → words fly into the product description',
    'product copywriting, review mining, product description tips','cro',S)
add(7,'CONNECTED-6','1-6','6 singles','NAVY','6 Instagram content ideas that sell for stores (in use, customer photo, behind the scenes, how it\'s made, FAQ answer, before/after)',
    'Don\'t know what to post for your store?','Each tile one idea with a phone post mockup; tile 6 CTA',
    'instagram content ideas for small business, shopify instagram, ecommerce content','social',S)
# ---------- Day 8 (Sun Dec 6) ----------
add(8,'L-N-L','LEFT','Carousel','LIGHT','First 60 days after an order: the email calendar (day 0, 3, 10, 21, 45, 60)',
    'What to send customers in the first 60 days.','Cover: timeline with 6 email chips',
    'customer retention emails, post purchase flow, email calendar','email',SV)
add(8,'L-N-L','MIDDLE','Reel','NAVY','Clean your email list: stop sending to people who never open',
    'Sending emails nobody opens? It hurts you.','0–2s: inbox with grey unopened stack, "Spam" folder blinks',
    'email list cleaning, email deliverability, ecommerce email','email',S)
add(8,'L-N-L','RIGHT','Single','LIGHT','Low stock shown honestly (only real numbers, never fake)',
    'Running low? Say it. Only if it\'s true.','Headline + product card with real stock line',
    'low stock alert, honest urgency, inventory display','trust',S)
add(8,'SIMILAR-3','RIGHT','Single','LIGHT','Small copy fix #3: one shipping line under the price',
    'Add one line under your price.','Tile: product card with "Free shipping over $50 · Arrives in 3–5 days"',
    'product page copy, shipping message, conversion copywriting','cro',SV)
add(8,'SIMILAR-3','MIDDLE','Single','LIGHT','Small copy fix #2: headline that says the benefit, not the product name',
    'Your homepage headline says nothing?','Tile: weak vs clear headline cards',
    'homepage headline, value proposition, shopify copywriting','cro',SV)
add(8,'SIMILAR-3','LEFT','Single','LIGHT','Small copy fix #1: button text that says what happens ("Add to cart", not "Submit")',
    'Your button says "Submit"? Change it.','Tile: two buttons, struck vs fixed',
    'button copy, call to action, shopify conversion tips','cro',SV)
add(8,'N-L-N','RIGHT','Reel','NAVY','Mistake: homepage video that autoplays with sound / huge and slow',
    'Your homepage video is chasing customers away.','0–2s: phone loads, big video spins, volume icon blasts',
    'homepage video, shopify speed, homepage design mistakes','design',S)
add(8,'N-L-N','MIDDLE','Single','LIGHT','Unboxing checklist: clean box, card, care guide, small extra, easy return info',
    'The unboxing is part of your product.','Headline + real-looking box contents with 5 chips',
    'unboxing experience, ecommerce packaging, brand experience','growth',S)
add(8,'N-L-N','LEFT','Reel','NAVY','Growth: watch 5 visitor recordings a week to see where they get stuck',
    'Watch your customers shop. Then fix it.','0–2s: cursor replay moves, stops, rage-taps a button',
    'session recordings, heatmaps shopify, find conversion problems','cro',S)
add(8,'CONNECTED-6','1-6','6 singles','LIGHT','6 checkout fixes (guest checkout, express pay, delivery date, fewer fields, returns line, code box)',
    'Customers get to checkout… then stop?','Each tile one fix with checkout UI; tile 6 CTA',
    'checkout optimization, shopify checkout, cart abandonment','cro',SV)
# ---------- Day 9 (Mon Dec 7) ----------
add(9,'L-N-L','LEFT','Carousel','LIGHT','A "Why buy from us" section: 3 promises you can keep, with proof',
    'Why should customers buy from you, not them?','Cover: section UI with 3 promise cards',
    'unique selling point, why choose us section, brand differentiation','growth',SV)
add(9,'L-N-L','MIDDLE','Reel','NAVY','Retargeting ads for cart abandoners: give a reason (reviews, delivery date), not just a discount',
    'They added to cart. Your ad should answer why.','0–2s: cart icon → ad card follows them on another app',
    'retargeting ads, abandoned cart ads, facebook retargeting','ads',S)
add(9,'L-N-L','RIGHT','Single','LIGHT','Local pickup & delivery options (say them on the product page)',
    'Customers nearby? Let them pick it up.','Headline + product page "Pick up today" option UI',
    'local pickup shopify, local delivery, small business shipping','growth',S)
add(9,'SIMILAR-3','RIGHT','Single','NAVY','Trust for new stores #3: clear policies linked in the footer',
    'New store? Make your policies easy to find.','Tile: footer UI with 4 policy links highlighted',
    'shopify policies, refund policy, new store trust','trust',SV)
add(9,'SIMILAR-3','MIDDLE','Single','NAVY','Trust for new stores #2: a real address and contact options',
    'Can customers see you\'re a real business?','Tile: contact block UI with address + email + reply time',
    'contact page, business credibility, new shopify store','trust',SV)
add(9,'SIMILAR-3','LEFT','Single','NAVY','Trust for new stores #1: real photos of you and your workspace',
    'New store? Show the people behind it.','Tile: About block with real team photo (brand photo)',
    'about us page, brand story, build trust online','trust',SV)
add(9,'N-L-N','RIGHT','Reel','NAVY','Mistake: a 404 page that\'s a dead end (no search, no best sellers)',
    'Broken link? Your 404 page loses the sale.','0–2s: tap a link → "Page not found" blank screen, cursor stuck',
    '404 page shopify, broken links, store navigation','design',S)
add(9,'N-L-N','MIDDLE','Single','LIGHT','Year-end store review: 5 numbers to look at (visitors, add to cart, orders, repeat customers, returns)',
    'Before 2027: check these 5 numbers.','Headline + 5 navy number cards (no invented values)',
    'ecommerce year end review, shopify analytics, store kpis','growth',SV)
add(9,'N-L-N','LEFT','Reel','NAVY','Growth: "Shop the look" / complete the set on product pages',
    'They bought the dress. Show what goes with it.','0–2s: dress page, "Complete the look" row snaps in with bag + sneaker',
    'shop the look, cross sell shopify, product recommendations','cro',S)
add(9,'CONNECTED-6','1-6','6 singles','NAVY','6 ways to bring holiday customers back in January (thank-you, how-to-use, review ask, new arrivals, list-only early access, gift card reminder)',
    'Holiday customers gone in January?','Each tile one idea with email UI; tile 6 CTA',
    'customer retention january, post holiday email, repeat customers','email',S)
# ---------- Day 10 (Tue Dec 8) ----------
add(10,'L-N-L','LEFT','Carousel','LIGHT','Tag products in your Instagram posts (Instagram Shopping basics for Shopify)',
    'Seen on Instagram. Can they tap to buy?','Cover: phone post with product tag bubble',
    'instagram shopping, tag products instagram, shopify instagram','social',SV)
add(10,'L-N-L','MIDDLE','Reel','NAVY','Plan January now: the slow month (clear goals, email list, new arrivals, best sellers restock)',
    'January is slow? Plan it this week.','0–2s: calendar flips to January, empty orders chart, then a plan list',
    'january sales slump, ecommerce planning, new year marketing','growth',S)
add(10,'L-N-L','RIGHT','Single','LIGHT','Rules for a clean New Year sale (real old price, clear end date, limited items)',
    'Planning a New Year sale? Keep it honest.','Headline + sale card UI with 3 rule chips',
    'new year sale, honest pricing, sale strategy','trust',SV)
add(10,'SIMILAR-3','RIGHT','Single','LIGHT','Clear old stock #3: an outlet collection, separate from the main shop',
    'Old stock? Give it its own corner.','Tile: menu UI with "Last chance" collection',
    'clearance sale, outlet collection, inventory clearance','growth',SV)
add(10,'SIMILAR-3','MIDDLE','Single','LIGHT','Clear old stock #2: a gift with purchase instead of a big discount',
    'Clear old stock without cheap discounts.','Tile: cart UI with "Free gift" line',
    'gift with purchase, clear inventory, avoid discounting','growth',SV)
add(10,'SIMILAR-3','LEFT','Single','LIGHT','Clear old stock #1: bundle slow sellers with best sellers',
    'Slow sellers? Pair them with your best seller.','Tile: bundle card with 2 products',
    'product bundles, slow moving inventory, increase order value','growth',SV)
add(10,'N-L-N','RIGHT','Reel','NAVY','Mistake: no sign the item was added (no cart drawer / message), customers tap twice or leave',
    'Tapped Add to cart… did it work?','0–2s: tap, nothing happens, tap again, cart shows 2',
    'add to cart confirmation, cart drawer shopify, user experience','cro',S)
add(10,'N-L-N','MIDDLE','Single','LIGHT','Write a short brand promise customers remember (one sentence, top of homepage)',
    'Explain your store in one line?','Headline + homepage hero UI with one-line promise',
    'brand promise, value proposition, shopify homepage','growth',SV)
add(10,'N-L-N','LEFT','Reel','NAVY','Growth: match your ad to the page it opens (same product, same words, same offer)',
    'Your ad and your page must match.','0–2s: ad card morphs into the product page, words line up',
    'ad landing page, facebook ads shopify, ad to page match','ads',S)
add(10,'CONNECTED-6','1-6','6 singles','LIGHT','6 things to fix before running ads in the new year (speed, reviews, matching page, delivery date, cart email, tracking)',
    'Running ads in January? Fix these first.','Each tile one fix with realistic UI; tile 6 free audit CTA',
    'before running ads, facebook ads checklist, shopify ads preparation','ads',SV)

rows = []
for d in sorted(T):
    date = D0 + datetime.timedelta(days=d - 1)
    for t in T[d]:
        t['date'] = date.isoformat(); t['weekday'] = date.strftime('%a'); rows.append(t)
order = {'L-N-L': 0, 'SIMILAR-3': 1, 'N-L-N': 2, 'CONNECTED-6': 3}
rows.sort(key=lambda r: (r['day'], order[r['row']]))
for i, r in enumerate(rows, 1): r['id'] = i
assert len(rows) == 100, len(rows)
for r in rows: assert len(r['hashtags'].split()) == 5
json.dump(rows, open('kit/plan/topic_plan.json', 'w'), indent=1)
# markdown for the autopilot
md = ['# 100-topic plan (owner request, 2026-11-28)', '',
 'Owner: "create 100 post topics and separate them to my daily schedule… captivating hooks that get attention, keywords that grow my page".',
 'Built from the niche research of 2026-11-28 (Reels reach non-followers; watch time in the first 2 s, DM sends and saves are what spread a post;',
 'our own Reels lose strangers in the first 1–3 s; images reach almost no one). How runs use it:',
 '- Each run takes the FIRST topic below for its row type with an empty Status (any day; earlier days first), and makes it.',
 '  SIMILAR-3 / N-L-N / L-N-L: the 3 topics of that row type and day together (RIGHT, MIDDLE, LEFT). CONNECTED-6: the day\'s theme.',
 '- Use the Hook as the design headline / first spoken line (rewrite only to fit ≤ 9 words, keep the meaning). Make the',
 '  "First 2 s" happen in the first frames: motion + the hook on screen at once, voice starts immediately (no slow slide-in).',
 '- Put 1–2 of the Keywords naturally in caption line 1–2, the on-screen text and the alt text (Instagram search reads them).',
 '- Use the listed 5 hashtags. End the caption with the Share/Save line, then the usual DM GROWTH + ecommwave.org lines.',
 '- After publishing, write `DONE <media ids>` in the Status column (edit this file) and commit with the log.',
 '- Everything else (looks, real photos, reel style, voice, covers, honesty: no invented numbers) follows PLAYBOOK/VOICE as usual.', '']
for d in sorted(T):
    date = D0 + datetime.timedelta(days=d - 1)
    md += [f'## Day {d} · {date.strftime("%a %b %-d")}', '',
           '| # | Row | Slot | Format | Look | Topic | Hook | First 2 s | Keywords | Hashtags | Share/Save | Status |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in [x for x in rows if x['day'] == d]:
        md.append(f"| {r['id']} | {r['row']} | {r['slot']} | {r['format']} | {r['look']} | {r['topic']} | {r['hook']} | {r['opener']} | {r['keywords']} | {r['hashtags']} | {r['trigger']} |  |")
    md.append('')
open('kit/TOPIC_PLAN.md', 'w').write('\n'.join(md))
import csv
with open('kit/plan/topic_plan.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['#','Day','Date','Row','Slot','Format','Look','Topic','Hook','First 2 seconds','Keywords','Hashtags','Share/Save line'])
    for r in rows: w.writerow([r['id'],r['day'],r['date'],r['row'],r['slot'],r['format'],r['look'],r['topic'],r['hook'],r['opener'],r['keywords'],r['hashtags'],r['trigger']])
print('ok', len(rows))
