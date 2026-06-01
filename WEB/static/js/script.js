const moeda = new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'});
let carrinho = [];
let pedidos = [
  {id:'EX-1048', cliente:'Marina Costa', entregador:'Carlos Henrique', status:'Saiu para entrega', saida:'14:05', entrega:'Prev. 14:48', total:137.60, codigo:true},
  {id:'EX-1047', cliente:'Bianca Alves', entregador:'Fernanda Alves', status:'Em separação', saida:'-', entrega:'-', total:89.30, codigo:false},
  {id:'EX-1046', cliente:'Luana Ribeiro', entregador:'João Pedro', status:'Entregue', saida:'12:20', entrega:'13:04', total:214.15, codigo:true},
  {id:'EX-1045', cliente:'Patrícia Lima', entregador:'Carlos Henrique', status:'Pedido recebido', saida:'-', entrega:'-', total:56.78, codigo:true},
  {id:'EX-1044', cliente:'Camila Martins', entregador:'Fernanda Alves', status:'Entregue', saida:'10:35', entrega:'11:18', total:302.42, codigo:false}
];

function qs(sel){return document.querySelector(sel)}
function qsa(sel){return [...document.querySelectorAll(sel)]}
function codigoAleatorio(){return Math.floor(1000+Math.random()*9000)}
function toast(msg){const el=qs('#toast'); el.textContent=msg; el.classList.add('show'); setTimeout(()=>el.classList.remove('show'),2600)}

function renderCarrinho(){
  const lista = qs('#cartList');
  const total = carrinho.reduce((s,item)=>s+(item.preco*item.qtd),0);
  qs('#cartTotal').textContent = moeda.format(total);
  qs('#itensBadge').textContent = `${carrinho.reduce((s,i)=>s+i.qtd,0)} itens`;
  if(carrinho.length===0){
    lista.className = 'cart-list empty';
    lista.textContent = 'Nenhum produto foi adicionado ainda.';
    return;
  }
  lista.className = 'cart-list';
  lista.innerHTML = carrinho.map((item,idx)=>`
    <div class="cart-item">
      <div><strong>${item.nome}</strong><small>Qtd. ${item.qtd} • ${moeda.format(item.preco)}</small></div>
      <span>${moeda.format(item.preco*item.qtd)}</span>
    </div>
  `).join('');
}

function addProduto(card){
  const nome = card.dataset.nome;
  const preco = Number(card.dataset.preco);
  const existente = carrinho.find(item=>item.nome===nome);
  if(existente) existente.qtd += 1;
  else carrinho.push({nome,preco,qtd:1});
  renderCarrinho();
  toast(`${nome} adicionado ao carrinho`);
}

function badgeStatus(status){
  const cls = status==='Entregue' ? 'green' : status==='Saiu para entrega' ? 'red' : 'blue';
  return `<span class="status-pill ${cls}">${status}</span>`;
}

function renderPedidos(){
  const busca = (qs('#buscaPedido')?.value || '').toLowerCase();
  const filtro = qs('#filtroStatus')?.value || 'todos';
  const filtrados = pedidos.filter(p=>{
    const texto = `${p.cliente} ${p.entregador} ${p.status} ${p.id}`.toLowerCase();
    return texto.includes(busca) && (filtro==='todos' || p.status===filtro);
  });
  const tbody = qs('#tabelaPedidos');
  if(!tbody) return;
  tbody.innerHTML = filtrados.map(p=>`
    <tr>
      <td>${p.id}</td>
      <td>${p.cliente}</td>
      <td>${p.entregador}</td>
      <td>${badgeStatus(p.status)}</td>
      <td>${p.saida}</td>
      <td>${p.entrega}</td>
      <td>${moeda.format(p.total)}</td>
    </tr>
  `).join('') || `<tr><td colspan="7">Nenhum pedido encontrado.</td></tr>`;
}

function atualizarKPIs(){
  const total = pedidos.reduce((s,p)=>s+p.total,0);
  const concluidas = pedidos.filter(p=>p.status==='Entregue').length;
  const codigo = pedidos.length ? Math.round((pedidos.filter(p=>p.codigo).length / pedidos.length)*100) : 0;
  qs('#kpiPedidos').textContent = pedidos.length;
  qs('#kpiFaturamento').textContent = moeda.format(total);
  qs('#kpiConcluidas').textContent = concluidas;
  qs('#kpiCodigo').textContent = `${codigo}%`;
  desenharGraficos();
}

function desenharBarChart(){
  const canvas = qs('#barChart'); if(!canvas) return;
  const ctx = canvas.getContext('2d'); const w=canvas.width, h=canvas.height;
  ctx.clearRect(0,0,w,h);
  const dados = [18,24,14,31,26,38,21];
  const labels = ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];
  const max = Math.max(...dados);
  const gap=22; const barW=(w - gap*(dados.length+1))/dados.length;
  ctx.lineWidth=1; ctx.strokeStyle='#e6ebf2'; ctx.fillStyle='#6b7688'; ctx.font='bold 13px Segoe UI, Arial';
  for(let i=0;i<5;i++){const y=30+i*42; ctx.beginPath(); ctx.moveTo(20,y); ctx.lineTo(w-20,y); ctx.stroke();}
  dados.forEach((v,i)=>{
    const x=gap+i*(barW+gap); const bh=(v/max)*(h-78); const y=h-42-bh;
    const grad=ctx.createLinearGradient(0,y,0,h-42); grad.addColorStop(0,'#e50914'); grad.addColorStop(1,'#ff8f2b');
    ctx.fillStyle=grad; roundRect(ctx,x,y,barW,bh,14); ctx.fill();
    ctx.fillStyle='#172033'; ctx.fillText(v,x+barW/2-8,y-8);
    ctx.fillStyle='#6b7688'; ctx.fillText(labels[i],x+barW/2-10,h-15);
  });
}

function desenharDonut(){
  const canvas = qs('#donutChart'); if(!canvas) return;
  const ctx = canvas.getContext('2d'); const w=canvas.width, h=canvas.height;
  ctx.clearRect(0,0,w,h);
  const cont = {
    'Entregue': pedidos.filter(p=>p.status==='Entregue').length,
    'Em rota': pedidos.filter(p=>p.status==='Saiu para entrega').length,
    'Pendente': pedidos.filter(p=>p.status!=='Entregue' && p.status!=='Saiu para entrega').length
  };
  const vals = Object.values(cont); const labels = Object.keys(cont); const colors=['#1aaa78','#e50914','#1346a0'];
  const total = vals.reduce((a,b)=>a+b,0) || 1;
  let start = -Math.PI/2; const cx=w/2, cy=h/2-6, r=82;
  vals.forEach((v,i)=>{const angle=(v/total)*Math.PI*2; ctx.beginPath(); ctx.moveTo(cx,cy); ctx.arc(cx,cy,r,start,start+angle); ctx.closePath(); ctx.fillStyle=colors[i]; ctx.fill(); start+=angle;});
  ctx.beginPath(); ctx.arc(cx,cy,48,0,Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();
  ctx.fillStyle='#172033'; ctx.font='900 28px Segoe UI, Arial'; ctx.textAlign='center'; ctx.fillText(total,cx,cy+7);
  ctx.font='bold 12px Segoe UI, Arial'; ctx.fillStyle='#6b7688'; ctx.fillText('pedidos',cx,cy+28);
  ctx.textAlign='left'; ctx.font='bold 13px Segoe UI, Arial';
  labels.forEach((label,i)=>{const y=24+i*24; ctx.fillStyle=colors[i]; ctx.fillRect(22,y,12,12); ctx.fillStyle='#172033'; ctx.fillText(`${label}: ${vals[i]}`,42,y+11);});
}

function roundRect(ctx,x,y,w,h,r){
  const rr=Math.min(r,w/2,h/2);
  ctx.beginPath();ctx.moveTo(x+rr,y);ctx.arcTo(x+w,y,x+w,y+h,rr);ctx.arcTo(x+w,y+h,x,y+h,rr);ctx.arcTo(x,y+h,x,y,rr);ctx.arcTo(x,y,x+w,y,rr);ctx.closePath();
}
function desenharGraficos(){desenharBarChart();desenharDonut();}

qsa('.product-card button').forEach(btn=>btn.addEventListener('click',()=>addProduto(btn.closest('.product-card'))));

qs('#pedidoForm')?.addEventListener('submit', async e => {
  e.preventDefault();

  const formulario = e.currentTarget;

  if (carrinho.length === 0) {
    toast('Adicione pelo menos um produto.');
    return;
  }

  const form = new FormData(formulario);

  const codigoAtivo = form.get('codigoSeguranca') === 'on';

  const dadosPedido = {
    cliente: form.get('cliente'),
    cpf: form.get('cpf'),
    telefone: form.get('telefone'),

    logradouro: form.get('logradouro'),
    numero: form.get('numero'),
    complemento: form.get('complemento'),
    bairro: form.get('bairro'),
    cidade: form.get('cidade'),

    observacao: form.get('observacao'),

    codigoSeguranca: codigoAtivo,

    produtos: carrinho.map(item => ({
      nome: item.nome,
      preco: item.preco,
      qtd: item.qtd
    }))
  };

  try {
    const resposta = await fetch('/api/pedidos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(dadosPedido)
    });

    const resultado = await resposta.json();

    if (!resposta.ok) {
      console.error(resultado);
      toast('Erro ao cadastrar pedido.');
      return;
    }

    const pedidoSalvo = resultado.pedido;

    pedidos.unshift({
      id: pedidoSalvo._id,
      cliente: pedidoSalvo.comprador.nome,
      entregador: pedidoSalvo.entregador.nome || 'Aguardando associação',
      status: 'Pedido recebido',
      saida: '-',
      entrega: pedidoSalvo.previsao_entrega || '-',
      total: pedidoSalvo.valor_total,
      codigo: pedidoSalvo.codigo_seguranca !== 'Desativado'
    });

    const securityPreview = qs('#securityPreview');

    if (securityPreview) {
      if (pedidoSalvo.codigo_seguranca !== 'Desativado') {
        securityPreview.textContent = `Código ${pedidoSalvo.codigo_seguranca}`;
      } else {
        securityPreview.textContent = 'Desativado pelo cliente';
      }
    }

    carrinho = [];

    renderCarrinho();
    renderPedidos();
    atualizarKPIs();

    formulario.reset();

    toast('Pedido cadastrado com sucesso!');

  } catch (erro) {
    console.error(erro);
    toast('Erro ao cadastrar pedido.');
  }
});

qs('#buscaPedido')?.addEventListener('input',renderPedidos);
qs('#filtroStatus')?.addEventListener('change',renderPedidos);
qs('#btnAtualizar')?.addEventListener('click',()=>{atualizarKPIs();toast('Painel atualizado.');});

renderCarrinho();renderPedidos();atualizarKPIs();
window.addEventListener('resize',()=>setTimeout(desenharGraficos,150));
