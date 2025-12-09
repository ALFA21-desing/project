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
  if(cart.length===0){ el.innerHTML = '<p>Your cart is empty.</p>'; totalEl.textContent = '$0.00'; return; }
  let total = 0;
  cart.forEach((item, index)=>{
    const lineTotal = (item.price||0) * (item.qty||1);
    total += lineTotal;
    const row = document.createElement('div');
    row.className = 'cart-row';
    row.draggable = true;
    row.dataset.index = index;
    row.innerHTML = `
      <div class="cart-title">🔄 ${escapeHtml(item.title)}</div>
      <div class="cart-price">$${(item.price||0).toFixed(2)}</div>
      <div class="cart-qty"><input type="number" min="1" value="${item.qty}" data-title="${escapeHtml(item.title)}"></div>
      <div class="cart-line">$${lineTotal.toFixed(2)}</div>
      <div class="cart-actions"><button class="remove" data-title="${escapeHtml(item.title)}">Remove</button></div>
    `;
    
    // Drag and drop handlers
    row.addEventListener('dragstart', handleDragStart);
    row.addEventListener('dragend', handleDragEnd);
    row.addEventListener('dragover', handleDragOver);
    row.addEventListener('drop', handleDrop);
    row.addEventListener('dragleave', handleDragLeave);
    
    el.appendChild(row);
  });
  totalEl.textContent = '$'+total.toFixed(2);
  el.querySelectorAll('input[data-title]').forEach(inp=>{
    inp.addEventListener('change', e=>{
      const t = e.target.dataset.title; const v = parseInt(e.target.value) || 1; changeQty(t, v);
    });
  });
  el.querySelectorAll('button.remove').forEach(btn=>{
    btn.addEventListener('click', e=>{ 
      const title = e.target.dataset.title;
      showModal(
        'Remove Item',
        `Are you sure you want to remove "${escapeHtml(title)}" from your cart?`,
        () => removeFromCart(title),
        true
      );
    });
  });
  });
}

let draggedElement = null;

function handleDragStart(e) {
  this.classList.add('dragging');
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragEnd(e) {
  this.classList.remove('dragging');
  document.querySelectorAll('.cart-row').forEach(row => {
    row.classList.remove('drag-over');
  });
}

function handleDragOver(e) {
  if (e.preventDefault) {
    e.preventDefault();
  }
  e.dataTransfer.dropEffect = 'move';
  return false;
}

function handleDrop(e) {
  if (e.stopPropagation) {
    e.stopPropagation();
  }
  
  if (draggedElement !== this) {
    const cart = loadCart();
    const draggedIndex = parseInt(draggedElement.dataset.index);
    const targetIndex = parseInt(this.dataset.index);
    
    // Reorder cart array
    const [removed] = cart.splice(draggedIndex, 1);
    cart.splice(targetIndex, 0, removed);
    
    saveCart(cart);
    renderCart();
    showToast('Cart order updated');
  }
  
  this.classList.remove('drag-over');
  return false;
}

function handleDragLeave(e) {
  this.classList.remove('drag-over');
}

function escapeHtml(s){ return String(s).replace(/[&<>"']/g, ch=>({
function escapeHtml(s){ return String(s).replace(/[&<>"']/g, ch=>({
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[ch])); }

document.addEventListener('click', function(e){
  const addBtn = e.target.closest('[data-add]');
  const fallbackBtn = e.target.closest('.btn.primary');
  if(!btn) return;
  // If inside checkout form, do not intercept
  const btn = addBtn || fallbackBtn;
  if(!btn) return;
  if(btn.closest && btn.closest('#checkout-form')) return;

  if(addBtn && addBtn.dataset.add && addBtn.dataset.add.toLowerCase() === 'false') return;

  if(!addBtn){
  e.preventDefault();
  }

  e.preventDefault();
  const card = btn.closest('.product-card') || btn.closest('.product-detail') || btn.closest('.product-info');
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
    price = Number(btn.dataset.price)||0;
  }
  addToCart({title, price, qty:1});
  try{ showToast && showToast('Añadido al carrito: '+title); }catch(e){ console.log('Añadido al carrito', title); }
});

document.addEventListener('DOMContentLoaded', ()=>{
  if(document.getElementById('cart-items')){
      window.nextStep = function(step) {
        // Validate current step
        const currentStep = document.querySelector('.checkout-step[style*="display: block"], .checkout-step:not([style])');
    renderCart();
    const form = document.getElementById('checkout-form');
    if(form) {
      window.nextStep = function(step) {
        const currentStep = document.querySelector('.checkout-step[style*="display: block"], .checkout-step:not([style])');
          } else {
            input.style.borderColor = '';
          }
        });
        
        if (!valid) {
          showToast('Please fill in all required fields');
          return;
        }
        
        // Hide current step
        document.querySelectorAll('.checkout-step').forEach(s => s.style.display = 'none');
        
          return;
        }
        
        document.querySelectorAll('.checkout-step').forEach(s => s.style.display = 'none');
        document.querySelector(`.checkout-step[data-step="${step}"]`).style.display = 'block';
        
        document.querySelectorAll('.step-indicator').forEach(ind => {
            ind.classList.remove('completed');
          } else {
            ind.classList.remove('active', 'completed');
          }
        });
        
        // If step 3, show review
        if (step === 3) {
          showOrderReview();
        }
        
        window.scrollTo({top: 0, behavior: 'smooth'});
      };
          }
        });
        
        if (step === 3) {
        document.querySelectorAll('.step-indicator').forEach(ind => {
          const indStep = parseInt(ind.dataset.step);
          if (indStep < step) {
            ind.classList.add('completed');
            ind.classList.remove('active');
          } else if (indStep === step) {
            ind.classList.add('active');
            ind.classList.remove('completed');
          } else {
            ind.classList.remove('active', 'completed');
          }
        });
        
        window.scrollTo({top: 0, behavior: 'smooth'});
      };
      
      function showOrderReview() {
        const data = new FormData(form);
        const cart = loadCart();
        const total = document.getElementById('cart-total')?.textContent || '$0.00';
        
        let reviewHTML = '<h5>Shipping Information</h5>';
        reviewHTML += `<p><strong>Name:</strong> ${escapeHtml(data.get('name'))}<br>`;
        reviewHTML += `<strong>Email:</strong> ${escapeHtml(data.get('email'))}<br>`;
        reviewHTML += `<strong>Address:</strong> ${escapeHtml(data.get('address'))}, ${escapeHtml(data.get('city'))}, ${escapeHtml(data.get('zip'))}<br>`;
        reviewHTML += `<strong>Country:</strong> ${escapeHtml(data.get('country'))}</p>`;
        
        reviewHTML += '<h5>Payment Information</h5>';
        reviewHTML += `<p><strong>Card:</strong> **** **** **** ${escapeHtml(data.get('cardNumber')).slice(-4)}<br>`;
        reviewHTML += `<strong>Name on Card:</strong> ${escapeHtml(data.get('cardName'))}</p>`;
        
        reviewHTML += '<h5>Order Items</h5><ul style="list-style:none;padding:0">';
        cart.forEach(item => {
          reviewHTML += `<li style="padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
            ${escapeHtml(item.title)} × ${item.qty} - $${((item.price||0) * (item.qty||1)).toFixed(2)}
          </li>`;
        });
        reviewHTML += `</ul><p style="font-size:1.2rem;font-weight:700;color:var(--accent)">Total: ${total}</p>`;
        
        document.getElementById('order-review').innerHTML = reviewHTML;
      }
      
      form.addEventListener('submit', function(e){
        e.preventDefault();
        const data = new FormData(form);
        const order = {
          name: data.get('name'), 
          email: data.get('email'), 
          address: data.get('address'),
          city: data.get('city'),
          zip: data.get('zip'),
          country: data.get('country'),
          phone: data.get('phone'),
          cart: loadCart(), 
          total: document.getElementById('cart-total')?.textContent || '',
          orderDate: new Date().toISOString()
        };
        
        // Save order to history
        const orders = JSON.parse(localStorage.getItem('order_history') || '[]');
        order.orderId = 'ORD-' + Date.now();
        orders.push(order);
        localStorage.setItem('order_history', JSON.stringify(orders));
        
          total: document.getElementById('cart-total')?.textContent || '',
          orderDate: new Date().toISOString()
        };
        
        const orders = JSON.parse(localStorage.getItem('order_history') || '[]');
        document.getElementById('checkout-form').style.display = 'none';
        document.getElementById('checkout-progress').style.display = 'none';
        orders.push(order);
        localStorage.setItem('order_history', JSON.stringify(orders));
        
        saveCart([]); 
        updateCartCount(); 
        renderCart();
        
        document.getElementById('checkout-form').style.display = 'none';
        document.getElementById('checkout-progress').style.display = 'none';
        
        document.getElementById('order-success').innerHTML = `
  // create toast container
  if(!document.getElementById('obelisco-toast')){
    const t = document.createElement('div'); t.id = 'obelisco-toast'; t.className = 'obelisco-toast'; document.body.appendChild(t);
  }
});

// Simple toast helper
function showToast(msg, ms=1800){
      });
    }
  }
  if(!document.getElementById('obelisco-toast')){

// Modal Dialog System
  }
});

function showToast(msg, ms=1800){s="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
  setTimeout(()=>{ el.style.opacity='0'; el.style.transform='translateY(10px)'; }, ms);
}

function createModal() {l-footer" id="modal-footer">
          <button class="btn" id="modal-cancel">Cancel</button>
          <button class="btn primary" id="modal-confirm">Confirm</button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // Close modal handlers
  document.getElementById('modal-close-btn').addEventListener('click', closeModal);
  document.getElementById('modal-cancel').addEventListener('click', closeModal);
  document.getElementById('obelisco-modal').addEventListener('click', function(e) {
    if (e.target.id === 'obelisco-modal') closeModal();
  });
}

function showModal(title, message, confirmCallback, showCancel = true) {
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  document.getElementById('modal-close-btn').addEventListener('click', closeModal);
  const confirmBtn = document.getElementById('modal-confirm');
  const cancelBtn = document.getElementById('modal-cancel');
  
  modalTitle.textContent = title;
  modalBody.innerHTML = message;
  cancelBtn.style.display = showCancel ? 'block' : 'none';
  
  // Remove old listeners and add new one
  const newConfirmBtn = confirmBtn.cloneNode(true);
  confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
  
  newConfirmBtn.addEventListener('click', function() {
    if (confirmCallback) confirmCallback();
  modalTitle.textContent = title;
  modalBody.innerHTML = message;
  cancelBtn.style.display = showCancel ? 'block' : 'none';
  
  const newConfirmBtn = confirmBtn.cloneNode(true);
function closeModal() {
  const modal = document.getElementById('obelisco-modal');
  if (modal) modal.classList.remove('active');
}
