const CART_KEY = 'obelisco_cart_v1';

function loadCart(){
  try{ return JSON.parse(localStorage.getItem(CART_KEY)) || []; }catch(e){ return []; }
}

function saveCart(cart){ 
  localStorage.setItem(CART_KEY, JSON.stringify(cart)); 
}

function updateCartCount(){
  const cart = loadCart();
  const count = cart.reduce((s,i)=>s+ (i.qty||1),0);
  document.querySelectorAll('#cart-count').forEach(el=>el.textContent = count);
}

function addToCart(item){
  const cart = loadCart();
  const found = cart.find(i=>i.title === item.title);
  if(found){ 
    found.qty = (found.qty||1) + (item.qty||1); 
  } else { 
    cart.push({title:item.title, price: Number(item.price)||0, qty: item.qty||1}); 
  }
  saveCart(cart);
  updateCartCount();
}

function removeFromCart(title){
  let cart = loadCart();
  cart = cart.filter(i=>i.title !== title);
  saveCart(cart); 
  updateCartCount(); 
  renderCart();
}

function changeQty(title, qty){
  const cart = loadCart();
  const it = cart.find(i=>i.title===title);
  if(it){ 
    it.qty = qty; 
    if(it.qty<1) it.qty =1; 
  }
  saveCart(cart); 
  updateCartCount(); 
  renderCart();
}

function escapeHtml(s){ 
  return String(s).replace(/[&<>"']/g, ch=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"
  }[ch])); 
}

function renderCart(){
  const cart = loadCart();
  const el = document.getElementById('cart-items');
  const totalEl = document.getElementById('cart-total');
  if(!el) return;
  
  el.innerHTML = '';
  if(cart.length===0){ 
    el.innerHTML = '<p>Your cart is empty.</p>'; 
    totalEl.textContent = '$0.00'; 
    return; 
  }
  
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
      const t = e.target.dataset.title; 
      const v = parseInt(e.target.value) || 1; 
      changeQty(t, v);
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
}

let draggedElement = null;

function handleDragStart(e) {
  draggedElement = this;
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
  this.classList.add('drag-over');
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

document.addEventListener('click', function(e){
  // Only respond to explicit add-to-cart triggers: elements with data-add="true"
  const addBtn = e.target.closest('[data-add="true"]');
  if(!addBtn) return;
  if(addBtn.closest && addBtn.closest('#checkout-form')) return;
  e.preventDefault();

  let title, price;
  const card = addBtn.closest('.product-card') || addBtn.closest('.product-detail') || addBtn.closest('.product-info');

  if(card){
    const tEl = card.querySelector('.product-title') || card.querySelector('.product-meta h1') || card.querySelector('h1');
    const pEl = card.querySelector('.product-price') || card.querySelector('.price');
    title = tEl ? tEl.textContent.trim() : (addBtn.dataset.title || 'Product');
    price = pEl ? parseFloat((pEl.textContent||'').replace(/[^0-9\.]/g,''))||0 : Number(addBtn.dataset.price)||0;
  } else {
    // If button is not inside a product card, require explicit dataset values to add
    if(addBtn.dataset && (addBtn.dataset.title || addBtn.dataset.price)){
      title = addBtn.dataset.title || 'Product';
      price = Number(addBtn.dataset.price)||0;
    } else {
      // Not a valid add-to-cart source; ignore click
      return;
    }
  }

  addToCart({title, price, qty:1});
  showToast('Added to cart: ' + title);
});

document.addEventListener('DOMContentLoaded', ()=>{
  updateCartCount();
  
  if(document.getElementById('cart-items')){
    renderCart();
    
    const form = document.getElementById('checkout-form');
    if(form) {
      setupCheckoutFlow();
      setupCardFormatting();
      
      window.goToShipping = function() {
        changeStep(1);
      };
      
      window.goToPayment = function() {
        if(validateStep(1)) {
          changeStep(2);
        }
      };
      
      window.goToReview = function() {
        if(validateStep(2)) {
          populateReviewStep();
          changeStep(3);
        }
      };
      
      window.nextStep = function(step) {
        const currentStep = document.querySelector('.checkout-step[style*="display: block"], .checkout-step:not([style])');
        
        if (currentStep) {
          const inputs = currentStep.querySelectorAll('input[required], select[required], textarea[required]');
          let valid = true;
          
          inputs.forEach(input => {
            if (!input.value.trim()) {
              valid = false;
              input.style.borderColor = '#e74c3c';
            } else {
              input.style.borderColor = '';
            }
          });
          
          if (!valid) {
            showToast('Please fill in all required fields');
            return;
          }
        }
        
        document.querySelectorAll('.checkout-step').forEach(s => s.style.display = 'none');
        const nextStepEl = document.querySelector('.checkout-step[data-step="' + step + '"]');
        if (nextStepEl) {
          nextStepEl.style.display = 'block';
        }
      };

      form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if(!validateStep(3)) return;
        
        const submitBtn = form.querySelector('button[type="submit"]');
        if(submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '⏳ Processing...';
        }
        
        setTimeout(() => {
          const cart = loadCart();
          const subtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
          const shipping = 15.00;
          const tax = subtotal * 0.08;
          const total = subtotal + shipping + tax;
          
          const orderDetails = {
            items: cart,
            subtotal: subtotal,
            shipping: shipping,
            tax: tax,
            total: total,
            firstName: document.getElementById('first-name')?.value || '',
            lastName: document.getElementById('last-name')?.value || '',
            email: document.getElementById('email')?.value || '',
            phone: document.getElementById('phone')?.value || '',
            address: document.getElementById('address')?.value || '',
            address2: document.getElementById('address2')?.value || '',
            city: document.getElementById('city')?.value || '',
            state: document.getElementById('state')?.value || '',
            zip: document.getElementById('zip')?.value || '',
            country: document.getElementById('country')?.value || '',
            cardLastFour: document.getElementById('card-number')?.value.replace(/\s/g, '').slice(-4) || '',
            orderNumber: 'ORD-' + Date.now(),
            orderDate: new Date().toLocaleString()
          };
          
          localStorage.setItem('last_order', JSON.stringify(orderDetails));
          
          saveCart([]);
          updateCartCount();
          
          document.getElementById('checkout-form').style.display = 'none';
          document.getElementById('checkout-progress').style.display = 'none';
          
          const successEl = document.getElementById('order-success');
          if(successEl) {
            successEl.style.display = 'block';
            successEl.innerHTML = `
              <div style="text-align:center;padding:60px 20px;animation:fadeIn 0.5s ease">
                <div style="width:120px;height:120px;margin:0 auto 30px;background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);border-radius:50%;display:flex;align-items:center;justify-content:center;animation:scaleIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)">
                  <div style="font-size:64px;color:white">✓</div>
                </div>
                
                <h2 style="color:#4ade80;margin-bottom:12px;font-size:32px;animation:slideInUp 0.5s ease 0.2s both">Order Placed Successfully!</h2>
                <p style="color:var(--muted);margin-bottom:8px;font-size:18px;animation:slideInUp 0.5s ease 0.3s both">Thank you, ${escapeHtml(orderDetails.firstName)} ${escapeHtml(orderDetails.lastName)}! 🎉</p>
                <p style="color:var(--muted);margin-bottom:40px;animation:slideInUp 0.5s ease 0.4s both">Your order has been received and will be processed soon.</p>
                
                <div style="background:rgba(255,255,255,0.03);padding:30px;border-radius:16px;margin-bottom:30px;max-width:500px;margin-left:auto;margin-right:auto;border:1px solid rgba(255,255,255,0.05);animation:slideInUp 0.5s ease 0.5s both">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:20px;border-bottom:2px solid rgba(255,255,255,0.1)">
                    <div style="text-align:left">
                      <div style="color:var(--muted);font-size:14px;margin-bottom:4px">Order Number</div>
                      <div style="color:var(--text);font-weight:700;font-size:18px">${orderDetails.orderNumber}</div>
                    </div>
                    <div style="text-align:right">
                      <div style="color:var(--muted);font-size:14px;margin-bottom:4px">Order Date</div>
                      <div style="color:var(--text);font-weight:500">${new Date().toLocaleDateString()}</div>
                    </div>
                  </div>
                  
                  <div style="margin-bottom:20px">
                    <div style="display:flex;justify-content:space-between;margin-bottom:10px">
                      <span style="color:var(--muted)">Subtotal:</span>
                      <span style="color:var(--text);font-weight:500">$${subtotal.toFixed(2)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:10px">
                      <span style="color:var(--muted)">Shipping:</span>
                      <span style="color:var(--text);font-weight:500">$${shipping.toFixed(2)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;margin-bottom:16px">
                      <span style="color:var(--muted)">Tax:</span>
                      <span style="color:var(--text);font-weight:500">$${tax.toFixed(2)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding-top:16px;border-top:2px solid rgba(255,255,255,0.1)">
                      <span style="font-size:20px;font-weight:700;color:var(--text)">Total:</span>
                      <span style="font-size:20px;font-weight:700;color:#4ade80">$${total.toFixed(2)}</span>
                    </div>
                  </div>
                  
                  <div style="text-align:left;padding:16px;background:rgba(255,255,255,0.02);border-radius:8px;margin-bottom:16px">
                    <div style="color:var(--muted);font-size:14px;margin-bottom:8px">📧 Confirmation Email</div>
                    <div style="color:var(--text);font-weight:500">${escapeHtml(orderDetails.email)}</div>
                  </div>
                  
                  <div style="text-align:left;padding:16px;background:rgba(255,255,255,0.02);border-radius:8px">
                    <div style="color:var(--muted);font-size:14px;margin-bottom:8px">🚚 Shipping Address</div>
                    <div style="color:var(--text);line-height:1.6">
                      ${escapeHtml(orderDetails.address)}${orderDetails.address2 ? ', ' + escapeHtml(orderDetails.address2) : ''}<br>
                      ${escapeHtml(orderDetails.city)}, ${escapeHtml(orderDetails.state)} ${escapeHtml(orderDetails.zip)}
                    </div>
                  </div>
                </div>
                
                <div style="display:flex;gap:12px;justify-content:center;animation:slideInUp 0.5s ease 0.6s both">
                  <a href="catalogo.html" class="btn primary" style="padding:14px 32px;font-size:16px">Continue Shopping 🛍️</a>
                  <a href="index.html" class="btn" style="padding:14px 32px;font-size:16px">Go Home</a>
                </div>
              </div>
            `;
          }
          
          confetti();
        }, 1500);
      });
    }
  }
});

function setupCheckoutFlow() {
  const steps = document.querySelectorAll('.step-indicator');
  steps.forEach(step => {
    step.addEventListener('click', function() {
      const stepNum = parseInt(this.dataset.step);
      if(stepNum < getCurrentStep()) {
        changeStep(stepNum);
      }
    });
  });
}

function getCurrentStep() {
  const activeStep = document.querySelector('.checkout-step[style*="display: block"], .checkout-step:not([style*="display: none"])');
  return activeStep ? parseInt(activeStep.dataset.step) : 1;
}

function changeStep(stepNum) {
  document.querySelectorAll('.checkout-step').forEach(s => {
    s.style.display = 'none';
  });
  
  const targetStep = document.querySelector('.checkout-step[data-step="' + stepNum + '"]');
  if(targetStep) {
    targetStep.style.display = 'block';
    targetStep.style.animation = 'slideInRight 0.3s ease';
  }
  
  document.querySelectorAll('.step-indicator').forEach((indicator, index) => {
    indicator.classList.remove('active', 'completed');
    const indicatorStep = parseInt(indicator.dataset.step);
    if(indicatorStep < stepNum) {
      indicator.classList.add('completed');
    } else if(indicatorStep === stepNum) {
      indicator.classList.add('active');
    }
  });
  
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function validateStep(stepNum) {
  const step = document.querySelector('.checkout-step[data-step="' + stepNum + '"]');
  if(!step) return false;
  
  const inputs = step.querySelectorAll('input[required], select[required], textarea[required]');
  let valid = true;
  let firstInvalid = null;
  
  inputs.forEach(input => {
    if(input.type === 'checkbox') {
      if(!input.checked) {
        valid = false;
        input.style.outline = '2px solid #e74c3c';
        if(!firstInvalid) firstInvalid = input;
      } else {
        input.style.outline = '';
      }
    } else {
      if(!input.value.trim()) {
        valid = false;
        input.style.borderColor = '#e74c3c';
        input.style.animation = 'shake 0.3s ease';
        if(!firstInvalid) firstInvalid = input;
      } else {
        input.style.borderColor = '';
        input.style.animation = '';
      }
    }
  });
  
  if(stepNum === 2) {
    const cardNumber = document.getElementById('card-number');
    const cardExpiry = document.getElementById('card-expiry');
    const cardCVV = document.getElementById('card-cvv');
    
    if(cardNumber && !validateCardNumber(cardNumber.value)) {
      valid = false;
      cardNumber.style.borderColor = '#e74c3c';
      if(!firstInvalid) firstInvalid = cardNumber;
    }
    
    if(cardExpiry && !validateExpiry(cardExpiry.value)) {
      valid = false;
      cardExpiry.style.borderColor = '#e74c3c';
      if(!firstInvalid) firstInvalid = cardExpiry;
    }
    
    if(cardCVV && (cardCVV.value.length < 3 || cardCVV.value.length > 4)) {
      valid = false;
      cardCVV.style.borderColor = '#e74c3c';
      if(!firstInvalid) firstInvalid = cardCVV;
    }
  }
  
  if(!valid) {
    showToast('❌ Please fill in all required fields correctly', 3000);
    if(firstInvalid) {
      firstInvalid.focus();
      firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
  
  return valid;
}

function validateCardNumber(number) {
  const cleaned = number.replace(/\s/g, '');
  return /^\d{13,19}$/.test(cleaned);
}

function validateExpiry(expiry) {
  if(!/^\d{2}\/\d{2}$/.test(expiry)) return false;
  const [month, year] = expiry.split('/').map(n => parseInt(n));
  return month >= 1 && month <= 12;
}

function setupCardFormatting() {
  const cardNumber = document.getElementById('card-number');
  const cardName = document.getElementById('card-name');
  const cardExpiry = document.getElementById('card-expiry');
  const cardCVV = document.getElementById('card-cvv');
  
  if(cardNumber) {
    cardNumber.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\s/g, '');
      let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
      e.target.value = formattedValue.substring(0, 19);
      
      const display = document.getElementById('card-number-display');
      if(display) {
        if(value.length > 0) {
          let masked = value.split('').map((char, i) => {
            return i < value.length - 4 ? '•' : char;
          }).join('');
          display.textContent = masked.match(/.{1,4}/g)?.join(' ') || masked;
        } else {
          display.textContent = '•••• •••• •••• ••••';
        }
      }
    });
  }
  
  if(cardName) {
    cardName.addEventListener('input', function(e) {
      const display = document.getElementById('card-name-display');
      if(display) {
        display.textContent = e.target.value.toUpperCase() || 'YOUR NAME';
      }
    });
  }
  
  if(cardExpiry) {
    cardExpiry.addEventListener('input', function(e) {
      let value = e.target.value.replace(/\D/g, '');
      if(value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
      }
      e.target.value = value;
      
      const display = document.getElementById('card-expiry-display');
      if(display) {
        display.textContent = value || 'MM/YY';
      }
    });
  }
  
  if(cardCVV) {
    cardCVV.addEventListener('input', function(e) {
      e.target.value = e.target.value.replace(/\D/g, '').substring(0, 4);
    });
  }
}

function populateReviewStep() {
  const cart = loadCart();
  const reviewDiv = document.getElementById('order-review');
  
  if(reviewDiv && cart.length > 0) {
    let total = 0;
    let itemsHTML = '<h5 style="margin-top:0;color:#000;font-size:16px;margin-bottom:16px">🛍️ Order Items</h5>';
    
    cart.forEach(item => {
      const lineTotal = item.price * item.qty;
      total += lineTotal;
      itemsHTML += `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
          <div>
            <div style="color:#000;font-weight:500">${escapeHtml(item.title)}</div>
            <div style="color:#000;font-size:14px">Quantity: ${item.qty} × $${item.price.toFixed(2)}</div>
          </div>
          <div style="color:#000;font-weight:600">$${lineTotal.toFixed(2)}</div>
        </div>
      `;
    });
    
    const shipping = 15.00;
    const tax = total * 0.08;
    const finalTotal = total + shipping + tax;
    
    itemsHTML += `
      <div style="margin-top:16px;padding-top:16px;border-top:2px solid rgba(255,255,255,0.1)">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:#000">
          <span>Subtotal:</span>
          <span>$${total.toFixed(2)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;color:#000">
          <span>Shipping:</span>
          <span>$${shipping.toFixed(2)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:12px;color:#000">
          <span>Tax (8%):</span>
          <span>$${tax.toFixed(2)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:20px;font-weight:700;color:#000">
          <span>Total:</span>
          <span>$${finalTotal.toFixed(2)}</span>
        </div>
      </div>
    `;
    
    reviewDiv.innerHTML = itemsHTML;
  }
  
  const shippingSummary = document.getElementById('shipping-summary');
  if(shippingSummary) {
    const firstName = document.getElementById('first-name')?.value || '';
    const lastName = document.getElementById('last-name')?.value || '';
    const email = document.getElementById('email')?.value || '';
    const phone = document.getElementById('phone')?.value || '';
    const address = document.getElementById('address')?.value || '';
    const address2 = document.getElementById('address2')?.value || '';
    const city = document.getElementById('city')?.value || '';
    const state = document.getElementById('state')?.value || '';
    const zip = document.getElementById('zip')?.value || '';
    const country = document.getElementById('country')?.selectedOptions[0]?.text || '';
    
    shippingSummary.innerHTML = `
      <div style="margin-bottom:8px"><strong style="color:#000">${escapeHtml(firstName)} ${escapeHtml(lastName)}</strong></div>
      <div style="color:#000">${escapeHtml(address)}${address2 ? ', ' + escapeHtml(address2) : ''}</div>
      <div style="color:#000">${escapeHtml(city)}, ${escapeHtml(state)} ${escapeHtml(zip)}</div>
      <div style="color:#000">${escapeHtml(country)}</div>
      <div style="margin-top:12px;color:#000">📧 ${escapeHtml(email)}</div>
      <div style="color:#000">📞 ${escapeHtml(phone)}</div>
    `;
  }
  
  const paymentSummary = document.getElementById('payment-summary');
  if(paymentSummary) {
    const cardNumber = document.getElementById('card-number')?.value || '';
    const cardName = document.getElementById('card-name')?.value || '';
    const lastFour = cardNumber.replace(/\s/g, '').slice(-4);
    
    paymentSummary.innerHTML = `
      <div style="display:flex;align-items:center;gap:12px">
        <div style="font-size:32px">💳</div>
        <div>
          <div style="color:#000;font-weight:500">${escapeHtml(cardName)}</div>
          <div style="color:#000">Card ending in ••••${lastFour}</div>
        </div>
      </div>
    `;
  }
}

function showToast(msg, ms=2000){
  if(!document.getElementById('obelisco-toast')){
    const t = document.createElement('div'); 
    t.id = 'obelisco-toast'; 
    t.className = 'obelisco-toast'; 
    document.body.appendChild(t);
  }
  
  const toast = document.getElementById('obelisco-toast');
  const el = document.createElement('div');
  el.textContent = msg;
  el.style.cssText = 'background:#27ae60;color:#fff;padding:12px 24px;border-radius:6px;margin-bottom:10px;opacity:0;transform:translateY(10px);transition:all 0.3s ease';
  toast.appendChild(el);
  
  setTimeout(()=>{ el.style.opacity='1'; el.style.transform='translateY(0)'; }, 10);
  setTimeout(()=>{ el.style.opacity='0'; el.style.transform='translateY(10px)'; }, ms);
  setTimeout(()=>{ el.remove(); }, ms + 300);
}

function createModal() {
  if (document.getElementById('obelisco-modal')) return;
  
  const modalHTML = `
    <div id="obelisco-modal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3 id="modal-title"></h3>
          <button class="modal-close" id="modal-close-btn">&times;</button>
        </div>
        <div class="modal-body" id="modal-body"></div>
        <div class="modal-footer" id="modal-footer">
          <button class="btn" id="modal-cancel">Cancel</button>
          <button class="btn primary" id="modal-confirm">Confirm</button>
        </div>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  document.getElementById('modal-close-btn').addEventListener('click', closeModal);
  document.getElementById('modal-cancel').addEventListener('click', closeModal);
  document.getElementById('obelisco-modal').addEventListener('click', function(e) {
    if (e.target.id === 'obelisco-modal') closeModal();
  });
}

function showModal(title, message, confirmCallback, showCancel = true) {
  if (!document.getElementById('obelisco-modal')) {
    createModal();
  }
  
  const modal = document.getElementById('obelisco-modal');
  const modalTitle = document.getElementById('modal-title');
  const modalBody = document.getElementById('modal-body');
  const confirmBtn = document.getElementById('modal-confirm');
  const cancelBtn = document.getElementById('modal-cancel');
  
  modalTitle.textContent = title;
  modalBody.innerHTML = message;
  cancelBtn.style.display = showCancel ? 'block' : 'none';
  
  const newConfirmBtn = confirmBtn.cloneNode(true);
  confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
  
  newConfirmBtn.addEventListener('click', function() {
    if (confirmCallback) confirmCallback();
    closeModal();
  });
  
  modal.classList.add('active');
}

function closeModal() {
  const modal = document.getElementById('obelisco-modal');
  if (modal) modal.classList.remove('active');
}

function confetti() {
  const colors = ['#667eea', '#764ba2', '#4ade80', '#fbbf24', '#f87171'];
  const confettiCount = 50;
  
  for(let i = 0; i < confettiCount; i++) {
    setTimeout(() => {
      const confettiPiece = document.createElement('div');
      confettiPiece.style.cssText = `
        position: fixed;
        width: 10px;
        height: 10px;
        background: ${colors[Math.floor(Math.random() * colors.length)]};
        top: -10px;
        left: ${Math.random() * 100}%;
        opacity: 1;
        transform: rotate(${Math.random() * 360}deg);
        z-index: 9999;
        pointer-events: none;
        border-radius: 50%;
      `;
      
      document.body.appendChild(confettiPiece);
      
      const duration = 2000 + Math.random() * 2000;
      const xMovement = (Math.random() - 0.5) * 200;
      
      confettiPiece.animate([
        { 
          transform: `translate(0, 0) rotate(0deg)`, 
          opacity: 1 
        },
        { 
          transform: `translate(${xMovement}px, 100vh) rotate(${Math.random() * 720}deg)`, 
          opacity: 0 
        }
      ], {
        duration: duration,
        easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
      });
      
      setTimeout(() => confettiPiece.remove(), duration);
    }, i * 30);
  }
}
