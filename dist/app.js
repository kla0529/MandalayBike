const $=s=>document.querySelector(s);
const paths={search:'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',heart:'<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/>',bag:'<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V2h6v2M9 10h6M9 14h6M9 18h4"/>'};
const icon=n=>`<svg viewBox="0 0 24 24" aria-hidden="true">${paths[n]||''}</svg>`;
$('#searchIcon').innerHTML=icon('search');$('#wishlistBtn').innerHTML=icon('heart');$('#bagIcon').innerHTML=icon('bag');
const copy={
  "en": {
    "myList": "My list",
    "showAtShop": "Show at shop",
    "editList": "Back to editing",
    "listPurpose": "Choose here. Show this list to our staff. Buy at the shop.",
    "reference": "Item",
    "quantityLabel": "Quantity",
    "shop": "Browse all",
    "hero": "Product catalog",
    "intro": "Browse items and prepare your buying list for the shop.",
    "explore": "Explore catalog",
    "collection": "THE COLLECTION",
    "collectionTitle": "Products",
    "allProducts": "All products",
    "saved": "Saved items",
    "sort": "Sort by:",
    "featured": "Featured",
    "low": "Price: low to high",
    "high": "Price: high to low",
    "nameSort": "Name: A–Z",
    "color": "Choose a color",
    "add": "Add to my list",
    "photoNote": "Confirm product details and availability at the shop.",
    "yourPicks": "READY FOR YOUR SHOP VISIT",
    "bag": "My buying list",
    "subtotal": "Estimated total",
    "cartNote": "Saved on this browser. Show this list at the shop to find and buy your items. Final prices and availability are confirmed in store.",
    "continue": "Browse more items",
    "search": "What are you looking for?",
    "items": "products",
    "inStock": "in stock",
    "noResults": "Nothing here just yet.",
    "trySearch": "Try another search or explore all products.",
    "reset": "Explore all products",
    "emptyBag": "Add items you want to buy, then show your list at the shop.",
    "added": "Added to your buying list",
    "remove": "Remove",
    "page": "Page",
    "of": "of",
    "colors": {
      "Red": "Red",
      "Blue": "Blue",
      "Black": "Black",
      "White": "White",
      "Silver": "Silver",
      "Green": "Green",
      "Brown": "Brown"
    },
    "branchLabel": "YOUR LOCAL BRANCH",
    "browsing": "Browse",
    "branchHint": "Prices, availability and your buying list belong to this branch.",
    "findBranches": "Find our branches",
    "aboutUs": "About us & branches",
    "visitUs": "COME SAY HELLO",
    "ourBranches": "Our branches",
    "addressPending": "Address to be added",
    "phonePending": "Phone number to be added",
    "hoursPending": "Opening hours to be added",
    "viberPending": "Viber link to be added",
    "facebookPending": "Facebook page to be added",
    "mapPending": "Map link to be added",
    "map": "Directions",
    "browseBranch": "Browse this branch",
    "currentBranch": "Currently browsing",
    "noInventory": "This branch’s inventory has not been uploaded yet.",
    "noInventoryText": "You can find its contact details below or browse another branch.",
    "viewContacts": "View branch details",
    "outOfStock": "Out of stock",
    "unavailable": "Unavailable at this branch",
    "limitedStock": "Available stock",
    "listNotice": "Items marked unavailable are excluded from the estimated total. Confirm your selections at the shop.",
    "listFor": "Buying list for",
    "branchChanged": "Branch changed. Each branch has its own buying list.",
    "loadError": "Unable to load the catalog. Please refresh and try again.",
    "category": "Category",
    "allCategories": "All categories"
  },
  "zh": {
    "myList": "购买清单",
    "showAtShop": "到店出示",
    "editList": "返回编辑",
    "listPurpose": "选好商品，到店出示清单给店员，再购买。",
    "reference": "编号",
    "quantityLabel": "数量",
    "shop": "全部商品",
    "hero": "商品目录",
    "intro": "浏览商品，准备好到店购买清单。",
    "explore": "浏览商品",
    "collection": "好物合集",
    "collectionTitle": "商品",
    "allProducts": "全部商品",
    "saved": "收藏商品",
    "sort": "排序：",
    "featured": "精选推荐",
    "low": "价格：从低到高",
    "high": "价格：从高到低",
    "nameSort": "名称：A–Z",
    "color": "选择颜色",
    "add": "加入购买清单",
    "photoNote": "请到店确认商品详情及库存。",
    "yourPicks": "为你的到店选购做好准备",
    "bag": "我的购买清单",
    "subtotal": "预计总价",
    "cartNote": "清单保存在当前浏览器。到店后出示给店员，确认商品、价格及库存，再购买。",
    "continue": "继续浏览商品",
    "search": "寻找你的心仪好物",
    "items": "件商品",
    "inStock": "件库存",
    "noResults": "暂时没有商品。",
    "trySearch": "试试其他关键词，或查看全部商品。",
    "reset": "查看全部商品",
    "emptyBag": "把想买的商品加入清单，到店出示给店员。",
    "added": "已加入购买清单",
    "remove": "移除",
    "page": "第",
    "of": "/",
    "colors": {
      "Red": "红色",
      "Blue": "蓝色",
      "Black": "黑色",
      "White": "白色",
      "Silver": "银色",
      "Green": "绿色",
      "Brown": "棕色"
    },
    "branchLabel": "你的附近分店",
    "browsing": "浏览",
    "branchHint": "商品价格、库存和购买清单均属于当前分店。",
    "findBranches": "查看全部分店",
    "aboutUs": "关于我们与分店",
    "visitUs": "欢迎到店",
    "ourBranches": "我们的分店",
    "addressPending": "地址待添加",
    "phonePending": "电话号码待添加",
    "hoursPending": "营业时间待添加",
    "viberPending": "Viber 链接待添加",
    "facebookPending": "Facebook 主页待添加",
    "mapPending": "地图链接待添加",
    "map": "路线导航",
    "browseBranch": "浏览这家分店",
    "currentBranch": "当前浏览",
    "noInventory": "这家分店暂未上传商品库存。",
    "noInventoryText": "你可以查看下方联系方式，或选择其他分店。",
    "viewContacts": "查看分店信息",
    "outOfStock": "暂时缺货",
    "unavailable": "当前分店暂无此商品",
    "limitedStock": "当前库存",
    "listNotice": "不可购买的商品未计入预计总价，请到店确认。",
    "listFor": "购买清单所属分店",
    "branchChanged": "已切换分店，每家分店都有独立的购买清单。",
    "loadError": "商品目录加载失败，请刷新重试。",
    "category": "分类",
    "allCategories": "全部分类"
  },
  "mm": {
    "myList": "စာရင်း",
    "showAtShop": "ဆိုင်တွင်ပြရန်",
    "editList": "စာရင်းပြင်ရန်",
    "listPurpose": "ပစ္စည်းရွေးပါ။ ဆိုင်ဝန်ထမ်းကိုစာရင်းပြပြီး ဆိုင်တွင်ဝယ်ပါ။",
    "reference": "ပစ္စည်း",
    "quantityLabel": "အရေအတွက်",
    "shop": "ပစ္စည်းအားလုံး",
    "hero": "ကုန်ပစ္စည်းစာရင်း",
    "intro": "ပစ္စည်းများကြည့်ပြီး ဆိုင်တွင်ဝယ်ယူရန် စာရင်းပြုလုပ်ပါ။",
    "explore": "ပစ္စည်းများကြည့်ရန်",
    "collection": "ပစ္စည်းစုစည်းမှု",
    "collectionTitle": "ကုန်ပစ္စည်းများ",
    "allProducts": "ပစ္စည်းအားလုံး",
    "saved": "သိမ်းထားသည်",
    "sort": "စီရန်",
    "featured": "ရွေးချယ်ထားသော",
    "low": "ဈေးနည်းမှများ",
    "high": "ဈေးများမှနည်း",
    "nameSort": "အမည် A–Z",
    "color": "အရောင်ရွေးရန်",
    "add": "ဝယ်မည့်စာရင်းထဲထည့်ရန်",
    "photoNote": "ပစ္စည်းအချက်အလက်နှင့် လက်ကျန်ကို ဆိုင်တွင်အတည်ပြုပါ။",
    "yourPicks": "ဆိုင်တွင်ပြရန် ရွေးထားသောပစ္စည်းများ",
    "bag": "ဝယ်မည့်ပစ္စည်းစာရင်း",
    "subtotal": "ခန့်မှန်းစုစုပေါင်း",
    "cartNote": "စာရင်းကို ဤဘရောက်ဇာတွင် သိမ်းထားသည်။ ဆိုင်တွင် ဤစာရင်းပြပြီး ပစ္စည်း၊ ဈေးနှုန်းနှင့် လက်ကျန်ကို အတည်ပြုကာ ဝယ်ယူပါ။",
    "continue": "ဆက်လက်ကြည့်ရန်",
    "search": "ဘာပစ္စည်းရှာနေပါသလဲ။",
    "items": "ပစ္စည်း",
    "inStock": "ခု ရှိသည်",
    "noResults": "ပစ္စည်းမတွေ့ပါ။",
    "trySearch": "အခြားစကားလုံးဖြင့် ရှာကြည့်ပါ။",
    "reset": "ပစ္စည်းအားလုံးကြည့်ရန်",
    "emptyBag": "ဝယ်လိုသောပစ္စည်းများထည့်ပြီး ဆိုင်တွင်စာရင်းပြပါ။",
    "added": "ဝယ်မည့်စာရင်းထဲထည့်ပြီးပါပြီ",
    "remove": "ဖယ်ရန်",
    "page": "စာမျက်နှာ",
    "of": "/",
    "colors": {
      "Red": "အနီ",
      "Blue": "အပြာ",
      "Black": "အနက်",
      "White": "အဖြူ",
      "Silver": "ငွေရောင်",
      "Green": "အစိမ်း",
      "Brown": "အညို"
    },
    "branchLabel": "သင်ရွေးထားသောဆိုင်ခွဲ",
    "browsing": "ကြည့်ရန်",
    "branchHint": "ဈေးနှုန်း၊ လက်ကျန်နှင့် ဝယ်မည့်စာရင်းသည် ဤဆိုင်ခွဲအတွက်ဖြစ်သည်။",
    "findBranches": "ဆိုင်ခွဲများကြည့်ရန်",
    "aboutUs": "ကျွန်ုပ်တို့နှင့် ဆိုင်ခွဲများ",
    "visitUs": "ဆိုင်သို့လာရောက်ပါ",
    "ourBranches": "ဆိုင်ခွဲများ",
    "addressPending": "လိပ်စာထည့်ရန်",
    "phonePending": "ဖုန်းနံပါတ်ထည့်ရန်",
    "hoursPending": "ဖွင့်ချိန်ထည့်ရန်",
    "viberPending": "Viber လင့်ခ်ထည့်ရန်",
    "facebookPending": "Facebook လင့်ခ်ထည့်ရန်",
    "mapPending": "မြေပုံလင့်ခ်ထည့်ရန်",
    "map": "လမ်းညွှန်",
    "browseBranch": "ဤဆိုင်ခွဲကိုကြည့်ရန်",
    "currentBranch": "ကြည့်နေသောဆိုင်ခွဲ",
    "noInventory": "ဤဆိုင်ခွဲ၏ပစ္စည်းစာရင်း မတင်ရသေးပါ။",
    "noInventoryText": "အောက်တွင် ဆက်သွယ်ရန်အချက်အလက်များကြည့်ပါ သို့မဟုတ် အခြားဆိုင်ခွဲရွေးပါ။",
    "viewContacts": "ဆိုင်ခွဲအချက်အလက်",
    "outOfStock": "ပစ္စည်းပြတ်နေသည်",
    "unavailable": "ဤဆိုင်ခွဲတွင်မရနိုင်ပါ",
    "limitedStock": "လက်ကျန်",
    "listNotice": "မရနိုင်သောပစ္စည်းများကို ခန့်မှန်းစုစုပေါင်းတွင် မထည့်ထားပါ။ ဆိုင်တွင်အတည်ပြုပါ။",
    "listFor": "ဝယ်မည့်စာရင်းအတွက် ဆိုင်ခွဲ",
    "branchChanged": "ဆိုင်ခွဲပြောင်းပြီးပါပြီ။ ဆိုင်ခွဲတစ်ခုစီတွင် သီးခြားဝယ်မည့်စာရင်းရှိသည်။",
    "loadError": "ပစ္စည်းစာရင်းဖွင့်မရပါ။ ပြန်လည်ဖွင့်ကြည့်ပါ။",
    "category": "အမျိုးအစား",
    "allCategories": "အမျိုးအစားအားလုံး"
  }
};
function readStore(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback}catch{return fallback}}
function saveStore(key,value){try{localStorage.setItem(key,JSON.stringify(value))}catch{}}
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=()=>copy[language];
const localized=value=>typeof value==='string'?value:value?.[language]||value?.en||'';
const name=p=>localized(p.name),desc=p=>localized(p.description);
const money=n=>new Intl.NumberFormat('en-US',{maximumFractionDigits:0}).format(n)+' Ks';
const key=(p,v)=>JSON.stringify([p,v]);
const placeholderImage='assets/product-placeholder.svg';
const productPhoto=(id,v)=>v?.image||placeholderImage;
// Missing product-code photos fall back in the browser, even before another build.
document.addEventListener('error',event=>{
 const img=event.target;
 if(!(img instanceof HTMLImageElement)||!img.hasAttribute('data-product-image'))return;
 const src=img.getAttribute('src'),fallback=img.dataset.fallbackSrc;
 if(fallback&&src!==fallback&&src!==placeholderImage)img.src=fallback;
 else if(src!==placeholderImage)img.src=placeholderImage;
},true);

let language=readStore('mb-language','mm');if(!copy[language])language='mm';
let catalog=null,branch=null,products=[],inventory=new Map(),allProducts=new Map();
let selectedCategory='',savedOnly=false,page=1,activeProduct=null,variantIndex=0,quantity=1;
let saved=readStore('mb-saved',[]),cart=[];
if(!Array.isArray(saved))saved=[];saved=saved.map(id=>typeof id==='number'?'MB-'+String(id).padStart(3,'0'):id);
function persistCart(){saveStore('mb-cart:'+branch.id,cart)}
function hydrateBranch(id,notify=false){
 branch=catalog.branches.find(b=>b.id===id)||catalog.branches[0];
 inventory=new Map(branch.inventory.map(v=>[key(v.productId,v.variantId),v]));
 const categoriesByProduct=new Map(branch.inventory.map(i=>[i.productId,i.category||'']));
 products=catalog.products.map(p=>({...p,category:categoriesByProduct.get(p.id)||p.category||'',variants:p.variants.map(v=>{const stock=inventory.get(key(p.id,v.id));return stock?{...v,price:stock.price,stock:stock.stock,image:stock.image||placeholderImage}:null}).filter(Boolean)})).filter(p=>p.variants.length);
 cart=readStore('mb-cart:'+branch.id,[]);if(!Array.isArray(cart))cart=[];
 // Migrate the original single-branch demo list once, without mixing branch lists.
 if(branch.id===catalog.branches[0].id&&!localStorageAvailableKey('mb-cart:'+branch.id)){
  const legacy=readStore('mb-cart',[]);
  if(Array.isArray(legacy))cart=legacy.flatMap(i=>{const p=catalog.products.find(p=>p.id==='MB-'+String(i.id).padStart(3,'0'));const v=p?.variants[i.variant];return v&&Number.isInteger(i.qty)&&i.qty>0?[{productId:p.id,variantId:v.id,qty:i.qty}]:[]});
  persistCart();
 }
 cart=cart.filter(i=>typeof i.productId==='string'&&typeof i.variantId==='string'&&Number.isInteger(i.qty)&&i.qty>0);
 saveStore('mb-branch',branch.id);selectedCategory='';savedOnly=false;page=1;$('#searchInput').value='';
 const url=new URL(location.href);url.searchParams.set('branch',branch.id);history.replaceState(null,'',url);
 updateLanguage();startHero();if(notify)toast(t().branchChanged);
}
function localStorageAvailableKey(key){try{return localStorage.getItem(key)!==null}catch{return true}}
function updateLanguage(){
 document.documentElement.lang=language==='mm'?'my':language;$('#language').value=language;
 document.querySelectorAll('[data-t]').forEach(el=>{if(t()[el.dataset.t])el.innerHTML=t()[el.dataset.t]});
 $('#searchInput').placeholder=t().search;saveStore('mb-language',language);
 if(!catalog)return;
 $('#branchSelect').innerHTML=catalog.branches.map(b=>`<option value="${escape(b.id)}">${escape(b.name)}</option>`).join('');$('#branchSelect').value=branch.id;
 $('#headerBranch').textContent='Mandalay Bike '+branch.name;document.title='Mandalay Bike '+branch.name+' — Catalog';
 renderCategories();render();renderCart();renderAbout();if(activeProduct&&$('#productModal').open)renderModal();
}
function firstVariant(p){return p.variants.find(v=>v.stock>0)||p.variants[0]}
function filtered(){
 const search=$('#searchInput').value.trim().toLowerCase();const result=products.filter(p=>(!selectedCategory||p.category===selectedCategory)&&(!savedOnly||saved.includes(p.id))&&(p.id+' '+Object.values(p.name).join(' ')).toLowerCase().includes(search));
 if($('#sortSelect').value==='low')result.sort((a,b)=>firstVariant(a).price-firstVariant(b).price);
 if($('#sortSelect').value==='high')result.sort((a,b)=>firstVariant(b).price-firstVariant(a).price);
 if($('#sortSelect').value==='name')result.sort((a,b)=>name(a).localeCompare(name(b)));
 return result;
}
function render(){
 const result=filtered(),pages=Math.max(1,Math.ceil(result.length/8));page=Math.min(page,pages);
 $('#collectionTitle').textContent=savedOnly?t().saved:t().collectionTitle;$('#resultCount').textContent=`${result.length} ${t().items}`;
 $('#allTab').classList.toggle('active',!savedOnly);$('#savedTab').classList.toggle('active',savedOnly);$('#wishlistBtn').setAttribute('aria-pressed',savedOnly);
 $('#productsGrid').innerHTML=result.slice((page-1)*8,page*8).map(p=>{const v=firstVariant(p);return `<article class="product-card"><div class="product-visual"><a href="#product-${encodeURIComponent(p.id)}" data-open="${escape(p.id)}" aria-label="${escape(name(p))}"><img data-product-image data-fallback-src="${escape(placeholderImage)}" src="${escape(productPhoto(p.id,v))}" alt="${escape(name(p))}" loading="lazy"></a><button class="save-btn ${saved.includes(p.id)?'saved':''}" data-save="${escape(p.id)}" aria-label="${escape(t().saved+': '+name(p))}" aria-pressed="${saved.includes(p.id)}">${icon('heart')}</button></div><div class="product-info">${p.category?`<div class="category-label">${escape(p.category)}</div>`:''}<h3><a href="#product-${encodeURIComponent(p.id)}" data-open="${escape(p.id)}">${escape(name(p))}</a></h3><p class="description">${escape(desc(p))}</p><div class="product-bottom"><span class="price">${money(v.price)}</span><button class="quick-add" data-open="${escape(p.id)}" aria-label="${escape(t().add+': '+name(p))}">+</button></div><p class="stock ${v.stock===0?'no-stock':''}">${v.stock>0?v.stock+' '+t().inStock:t().outOfStock}</p></div></article>`}).join('')||`<div class="empty"><h3>${branch.hasInventory?t().noResults:t().noInventory}</h3><p>${branch.hasInventory?t().trySearch:t().noInventoryText}</p>${branch.hasInventory?`<button class="button primary" id="resetFilters">${t().reset}</button>`:`<a class="button primary" href="#about">${t().viewContacts}</a>`}</div>`;
 $('#pageInfo').textContent=`${t().page} ${page} ${t().of} ${pages}`;$('#pageNumber').textContent=page;$('#prevBtn').disabled=page===1;$('#nextBtn').disabled=page===pages;
}
function openProduct(id){activeProduct=products.find(p=>p.id===id);if(!activeProduct)return;quantity=1;variantIndex=Math.max(0,activeProduct.variants.findIndex(v=>v.stock>0));renderModal();$('#productModal').showModal()}
function renderModal(){
 const p=activeProduct,v=p.variants[variantIndex];$('#modalBranch').textContent=branch.name;$('#modalCategory').textContent=p.category||'';$('#modalTitle').textContent=name(p);$('#modalDescription').textContent=desc(p);$('#modalImage').setAttribute('data-product-image','');$('#modalImage').dataset.fallbackSrc=placeholderImage;$('#modalImage').src=productPhoto(p.id,v);$('#modalImage').alt=name(p);$('#modalPrice').textContent=money(v.price);$('#modalStock').textContent=v.stock>0?v.stock+' '+t().inStock:t().outOfStock;$('#quantity').textContent=quantity;$('#decrease').disabled=quantity<=1;$('#increase').disabled=quantity>=v.stock;$('#modalAddBtn').disabled=v.stock<=0;$('#modalAddBtn').textContent=v.stock>0?t().add:t().outOfStock;
 $('#colorOptions').innerHTML=p.variants.map((v,i)=>`<button class="${i===variantIndex?'active':''}" data-variant="${i}" aria-pressed="${i===variantIndex}">${escape(t().colors[v.color]||v.color)}</button>`).join('');
}
let toastTimer;function toast(message){$('#toast').textContent=message;$('#toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),2800)}
function addToCart(){
 const p=activeProduct,v=p.variants[variantIndex];if(v.stock<=0)return;
 const item=cart.find(i=>i.productId===p.id&&i.variantId===v.id);if(item)item.qty=Math.min(v.stock,item.qty+quantity);else cart.push({productId:p.id,variantId:v.id,qty:quantity});
 persistCart();renderCart();$('#productModal').close();toast(t().added);
}
function resolveItem(i){const p=allProducts.get(i.productId),v=p?.variants.find(v=>v.id===i.variantId),stock=inventory.get(key(i.productId,i.variantId));return{p,v,stock}}
function renderCart(){
 let total=0,count=0,unavailable=false;$('#listBranch').textContent=t().listFor+': Mandalay Bike '+branch.name;
 $('#cartItems').innerHTML=cart.map((i,index)=>{
  const {p,v,stock}=resolveItem(i);const available=stock&&stock.stock>0;count+=i.qty;if(available)total+=stock.price*i.qty;else unavailable=true;
  return `<div class="cart-item ${available?'':'unavailable-item'}"><img data-product-image data-fallback-src="${escape(placeholderImage)}" src="${escape(productPhoto(i.productId,stock||v))}" alt="${escape(p?name(p):i.productId)}"><div><h3>${escape(p?name(p):i.productId)}</h3><p>${escape(t().reference+' '+i.productId+' · '+(t().colors[v?.color]||v?.color||i.variantId))}</p><p>${t().quantityLabel}: ${i.qty}${available?' × '+money(stock.price):''}</p>${!available?`<p class="availability-warning">${t().unavailable}</p>`:i.qty>stock.stock?`<p class="availability-warning">${t().limitedStock}: ${stock.stock}</p>`:''}<div class="list-quantity"><button data-list-step="-1" data-list-index="${index}" ${i.qty<=1?'disabled':''} aria-label="Decrease quantity">−</button><span>${i.qty}</span><button data-list-step="1" data-list-index="${index}" ${!available||i.qty>=stock.stock?'disabled':''} aria-label="Increase quantity">+</button></div><strong>${available?money(stock.price*i.qty):'—'}</strong></div><button data-remove="${index}">${t().remove}</button></div>`;
 }).join('')||`<p class="small">${t().emptyBag}</p>`;
 if(unavailable)$('#cartItems').insertAdjacentHTML('beforeend',`<p class="availability-warning">${t().listNotice}</p>`);
 $('#cartCount').textContent=count;$('#cartTotal').textContent=money(total);$('#showAtShop').disabled=!cart.length;
}
function contactLink(url,label,pending){return url?`<a href="${escape(url)}" target="_blank" rel="noopener noreferrer">${escape(label)} ↗</a>`:`<span class="contact-pending">${escape(pending)}</span>`}
function phoneLink(phone){const tel=phone.replace(/[^+0-9]/g,'');return tel?`<a href="tel:${escape(tel)}">${escape(phone)}</a>`:`<span class="contact-pending">${t().phonePending}</span>`}
function renderAbout(){
 $('#aboutTitle').textContent=localized(catalog.about.title);$('#aboutStory').textContent=localized(catalog.about.story);
 $('#mainContacts').innerHTML=`${phoneLink(catalog.about.phone||'')}${contactLink(catalog.about.viberUrl,'Viber',t().viberPending)}${contactLink(catalog.about.facebookUrl,'Facebook',t().facebookPending)}`;
 $('#branchCards').innerHTML=catalog.branches.map(b=>{const c=b.contact;return `<article class="branch-card ${branch.id===b.id?'selected-branch':''}"><div class="eyebrow">${escape(b.name)}</div><h4>Mandalay Bike ${escape(b.name)}</h4><p class="address">${escape(c.address||t().addressPending)}</p><p class="opening-hours">${escape(c.hours||t().hoursPending)}</p><div class="branch-contact-links">${phoneLink(c.phone)}${contactLink(c.viberUrl||catalog.about.viberUrl,'Viber',t().viberPending)}${contactLink(c.facebookUrl||catalog.about.facebookUrl,'Facebook',t().facebookPending)}${contactLink(c.mapUrl,t().map,t().mapPending)}</div><a class="branch-browse" href="?branch=${encodeURIComponent(b.id)}#catalog" data-branch="${escape(b.id)}">${branch.id===b.id?t().currentBranch:t().browseBranch} →</a></article>`}).join('');
}
document.addEventListener('click',e=>{
 const open=e.target.closest('[data-open]'),save=e.target.closest('[data-save]'),variant=e.target.closest('[data-variant]'),remove=e.target.closest('[data-remove]'),branchLink=e.target.closest('[data-branch]');
 if(open){e.preventDefault();openProduct(open.dataset.open)}
 if(save){const id=save.dataset.save;saved=saved.includes(id)?saved.filter(x=>x!==id):[...saved,id];saveStore('mb-saved',saved);render()}
 if(variant){variantIndex=Number(variant.dataset.variant);quantity=1;renderModal()}
 if(remove){cart.splice(Number(remove.dataset.remove),1);persistCart();renderCart()}
 if(branchLink){e.preventDefault();hydrateBranch(branchLink.dataset.branch,true);const branchUrl=new URL(location.href);branchUrl.hash='catalog';history.replaceState(null,'',branchUrl);$('#catalog').scrollIntoView({behavior:'smooth'})}
 if(e.target.closest('#resetFilters')){selectedCategory='';renderCategories();savedOnly=false;$('#searchInput').value='';page=1;render()}
});
$('#categoryFilter').onchange=e=>{selectedCategory=e.target.value;page=1;render()};
$('#branchSelect').onchange=e=>hydrateBranch(e.target.value,true);
$('#language').onchange=e=>{language=e.target.value;updateLanguage()};$('.search').onsubmit=e=>e.preventDefault();$('#searchInput').oninput=()=>{page=1;render()};$('#sortSelect').onchange=()=>{page=1;render()};$('#allTab').onclick=()=>{savedOnly=false;page=1;render()};
function showSaved(){savedOnly=true;page=1;render();$('#catalog').scrollIntoView({behavior:'smooth'})}
$('#savedTab').onclick=showSaved;$('#wishlistBtn').onclick=showSaved;$('#prevBtn').onclick=()=>{page--;render();$('#catalog').scrollIntoView()};$('#nextBtn').onclick=()=>{page++;render();$('#catalog').scrollIntoView()};
$('#closeModal').onclick=()=>$('#productModal').close();$('#closeCart').onclick=()=>$('#cartModal').close();$('#continueShopping').onclick=()=>$('#cartModal').close();$('#cartBtn').onclick=()=>{$('#cartModal').classList.remove('shop-view');renderCart();$('#cartModal').showModal()};
 document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}}));
$('#decrease').onclick=()=>{quantity=Math.max(1,quantity-1);renderModal()};$('#increase').onclick=()=>{quantity=Math.min(activeProduct.variants[variantIndex].stock,quantity+1);renderModal()};$('#modalAddBtn').onclick=addToCart;$('#year').textContent=new Date().getFullYear();
$('#showAtShop').onclick=()=>{$('#cartModal').classList.add('shop-view');$('#cartModal').scrollTop=0;$('#editList').focus()};$('#editList').onclick=()=>{$('#cartModal').classList.remove('shop-view');$('#showAtShop').focus()};
$('#cartItems').addEventListener('click',e=>{const b=e.target.closest('[data-list-step]');if(!b)return;const i=cart[Number(b.dataset.listIndex)],{stock}=resolveItem(i);if(!stock||stock.stock<=0)return;i.qty=Math.max(1,Math.min(stock.stock,i.qty+Number(b.dataset.listStep)));persistCart();renderCart()});
async function init(){
 try{const response=await fetch('catalog.json',{cache:'no-store'});if(!response.ok)throw Error('Catalog unavailable');catalog=await response.json();if(catalog.schemaVersion!==1||!catalog.branches.length)throw Error('Invalid catalog');allProducts=new Map(catalog.products.map(p=>[p.id,p]));const requested=new URL(location.href).searchParams.get('branch')||readStore('mb-branch','');hydrateBranch(requested)}
 catch(error){$('#productsGrid').innerHTML='<div class="empty"><h3>'+escape(t().loadError)+'</h3></div>';console.error(error)}
}


function renderCategories(){
 const values=[...new Set(products.map(p=>p.category).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
 if(!values.includes(selectedCategory))selectedCategory='';
 $('#categoryFilter').innerHTML='<option value="">'+escape(t().allCategories)+'</option>'+values.map(c=>'<option value="'+escape(c)+'">'+escape(c)+'</option>').join('');
 $('#categoryFilter').value=selectedCategory;
}
let heroTimer=null,lastHero='';
function startHero(){
 clearInterval(heroTimer);lastHero='';
 const photos=products.flatMap(p=>p.variants.map(v=>({src:v.image,name:name(p)}))).filter(p=>p.src&&p.src!==placeholderImage);
 const unique=[...new Map(photos.map(p=>[p.src,p])).values()];
 const image=$('#heroImage');
 if(!unique.length){image.src=placeholderImage;image.alt='';image.closest('.hero-visual').hidden=true;return}
 image.closest('.hero-visual').hidden=false;
 const advance=()=>{const pool=unique.length>1?unique.filter(p=>p.src!==lastHero):unique;const photo=pool[Math.floor(Math.random()*pool.length)];lastHero=photo.src;image.src=photo.src;image.alt=photo.name};
 image.onerror=()=>{image.src=placeholderImage;image.onerror=null};
 advance();if(unique.length>1&&!window.matchMedia('(prefers-reduced-motion: reduce)').matches)heroTimer=setInterval(advance,6000);
}

updateLanguage();init();
