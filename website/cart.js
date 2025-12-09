// Cart functionality: store cart in localStorage and render cart page
const CART_KEY = 'obelisco_cart_v1';

function loadCart(){
  try{ return JSON.parse(localStorage.getItem(CART_KEY)) || []; }catch(e){ return []; }
}
function saveCart(cart){ localStorage.setItem(CART_KEY, JSON.stringify(cart)); }

function updateCartCount(){
  const cart = loadCart();
  const count = cart.reduce((s,i)=>s+ (i.qty||1),0);
  document.querySelectorAll('#cart-count').forEach(el=>el.textContent = count);
}

function addToCart(item){
  const cart = loadCart();
  const found = cart.find(i=>i.title === item.title);
  if(found){ found.qty = (found.qty||1) + (item.qty||1); }
  else { cart.push({title:item.title, price: Number(item.price)||0, qty: item.qty||1}); }
  saveCart(cart);
  updateCartCount();
}

function removeFromCart(title){
  let cart = loadCart();
  cart = cart.filter(i=>i.title !== title);
  saveCart(cart); updateCartCount(); renderCart();
}

function changeQty(title, qty){
  const cart = loadCart();
  const it = cart.find(i=>i.title===title);
  if(it){ it.qty = qty; if(it.qty<1) it.qty =1; }
  saveCart(cart); updateCartCount(); renderCart();
}

function renderCart(){
  const cart = loadCart();
  const el = document.getElementById('cart-items');
  const totalEl = document.getElementById('cart-total');
  if(!el) return;
  el.innerHTML = '';
  if(cart.length===0){ el.innerHTML = '<p>Tu carrito está vacío.</p>'; totalEl.textContent = '$0.00'; return; }
  let total = 0;
  cart.forEach(item=>{
    const lineTotal = (item.price||0) * (item.qty||1);
    total += lineTotal;
    const row = document.createElement('div');
    row.className = 'cart-row';
    row.innerHTML = `
      <div class="cart-title">${escapeHtml(item.title)}</div>
      <div class="cart-price">$${(item.price||0).toFixed(2)}</div>
      <div class="cart-qty"><input type="number" min="1" value="${item.qty}" data-title="${escapeHtml(item.title)}"></div>
      <div class="cart-line">$${lineTotal.toFixed(2)}</div>
      <div class="cart-actions"><button class="remove" data-title="${escapeHtml(item.title)}">Eliminar</button></div>
    `;
    el.appendChild(row);
  });
  totalEl.textContent = '$'+total.toFixed(2);
  // attach qty listeners
  el.querySelectorAll('input[data-title]').forEach(inp=>{
    inp.addEventListener('change', e=>{
      const t = e.target.dataset.title; const v = parseInt(e.target.value) || 1; changeQty(t, v);
    });
  });
  el.querySelectorAll('button.remove').forEach(btn=>{
    btn.addEventListener('click', e=>{ removeFromCart(e.target.dataset.title); });
  });
}

function escapeHtml(s){ return String(s).replace(/[&<>"']/g, ch=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[ch])); }

// Delegated add-to-cart: look for .btn.primary clicks and read nearby product info
document.addEventListener('click', function(e){
  // Prefer explicit data attribute for add-to-cart buttons
  const addBtn = e.target.closest('[data-add]');
  // Fallback: button with .btn.primary outside checkout form and not inside cart page
  const fallbackBtn = e.target.closest('.btn.primary');
  const btn = addBtn || fallbackBtn;
  if(!btn) return;
  // If inside checkout form, do not intercept
  if(btn.closest && btn.closest('#checkout-form')) return;

  // If explicit opt-in required and present but set to false, skip
  if(addBtn && addBtn.dataset.add && addBtn.dataset.add.toLowerCase() === 'false') return;

  // If we fell back to .btn.primary, ensure its text suggests purchase
  if(!addBtn){
    if(!/comprar|agregar|add to cart|buy/i.test(btn.textContent)) return;
  }

  e.preventDefault();
  // try to find product info
  const card = btn.closest('.product-card') || btn.closest('.product-detail') || btn.closest('.product-info');
  let title = '';
  let price = 0;
  if(card){
    const tEl = card.querySelector('.product-title') || document.querySelector('.product-meta h1');
    const pEl = card.querySelector('.product-price') || card.querySelector('.price');
    title = tEl ? tEl.textContent.trim() : (btn.dataset.title || 'Producto');
    if(pEl) price = parseFloat((pEl.textContent||'').replace(/[^0-9\.]/g,''))||0;
  } else {
    title = btn.dataset.title || 'Producto';
    price = Number(btn.dataset.price)||0;
  }
  addToCart({title, price, qty:1});
  // small feedback via toast
  try{ showToast && showToast('Añadido al carrito: '+title); }catch(e){ console.log('Añadido al carrito', title); }
});

// If on cart page, render and handle checkout
document.addEventListener('DOMContentLoaded', ()=>{
  updateCartCount();
  if(document.getElementById('cart-items')){
    renderCart();
    const form = document.getElementById('checkout-form');
    form && form.addEventListener('submit', function(e){
      e.preventDefault();
      const data = new FormData(form);
      const order = {
        name: data.get('name'), email: data.get('email'), address: data.get('address'), cart: loadCart(), total: document.getElementById('cart-total')?.textContent || ''
      };
      // simulate order submission
      console.log('Order created', order);
      // clear cart
      saveCart([]); updateCartCount(); renderCart();
      document.getElementById('order-success').innerHTML = '<h3>Pedido recibido. Gracias, '+escapeHtml(order.name)+'.</h3><p>Revisaremos tu pedido y te contactaremos.</p>';
      form.reset();
    });
  }
  // create toast container
  if(!document.getElementById('obelisco-toast')){
    const t = document.createElement('div'); t.id = 'obelisco-toast'; t.className = 'obelisco-toast'; document.body.appendChild(t);
  }
});

// Simple toast helper
function showToast(msg, ms=1800){
  const el = document.getElementById('obelisco-toast');
  if(!el) return alert(msg);
  el.textContent = msg; el.style.opacity = '1'; el.style.transform = 'translateY(0)';
  setTimeout(()=>{ el.style.opacity='0'; el.style.transform='translateY(10px)'; }, ms);
}
