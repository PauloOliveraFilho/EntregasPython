const moeda = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL'
});

let carrinho = [];

function qs(seletor) {
  return document.querySelector(seletor);
}

function qsa(seletor) {
  return [...document.querySelectorAll(seletor)];
}

function toast(mensagem) {
  const el = qs('#toast');

  if (!el) {
    alert(mensagem);
    return;
  }

  el.textContent = mensagem;
  el.classList.add('show');

  setTimeout(() => {
    el.classList.remove('show');
  }, 2600);
}

function renderCarrinho() {
  const lista = qs('#cartList');
  const totalEl = qs('#cartTotal');
  const badgeEl = qs('#itensBadge');

  if (!lista || !totalEl || !badgeEl) {
    return;
  }

  const total = carrinho.reduce((soma, item) => {
    return soma + (item.preco * item.qtd);
  }, 0);

  const quantidadeItens = carrinho.reduce((soma, item) => {
    return soma + item.qtd;
  }, 0);

  totalEl.textContent = moeda.format(total);
  badgeEl.textContent = `${quantidadeItens} itens`;

  if (carrinho.length === 0) {
    lista.className = 'cart-list empty';
    lista.textContent = 'Nenhum produto foi adicionado ainda.';
    return;
  }

  lista.className = 'cart-list';

  lista.innerHTML = carrinho.map((item, indice) => `
    <div class="cart-item">
      <div>
        <strong>${item.nome}</strong>
        <small>Qtd. ${item.qtd} • ${moeda.format(item.preco)}</small>
      </div>

      <div>
        <span>${moeda.format(item.preco * item.qtd)}</span>
        <button type="button" class="btn-remover" onclick="removerItem(${indice})">Remover</button>
      </div>
    </div>
  `).join('');
}

function adicionarProduto(card) {
  const nome = card.dataset.nome;
  const preco = Number(card.dataset.preco);

  const produtoExistente = carrinho.find(item => item.nome === nome);

  if (produtoExistente) {
    produtoExistente.qtd += 1;
  } else {
    carrinho.push({
      nome: nome,
      preco: preco,
      qtd: 1
    });
  }

  renderCarrinho();
  toast(`${nome} adicionado ao carrinho.`);
}

function removerItem(indice) {
  carrinho.splice(indice, 1);
  renderCarrinho();
}

qsa('.product-card button').forEach(botao => {
  botao.addEventListener('click', () => {
    const card = botao.closest('.product-card');
    adicionarProduto(card);
  });
});

function atualizarTextoCodigoSeguranca() {
  const checkbox = qs('input[name="codigoSeguranca"]');
  const securityPreview = qs('#securityPreview');

  if (!checkbox || !securityPreview) {
    return;
  }

  if (checkbox.checked) {
    securityPreview.textContent = 'Código será gerado';
  } else {
    securityPreview.textContent = 'Código de segurança não solicitado';
  }
}

qs('input[name="codigoSeguranca"]')?.addEventListener('change', atualizarTextoCodigoSeguranca);

qs('#pedidoForm')?.addEventListener('submit', async evento => {
  evento.preventDefault();

  const formulario = evento.currentTarget;

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

    const securityPreview = qs('#securityPreview');

    if (securityPreview) {
      if (pedidoSalvo.codigo_seguranca !== 'Desativado') {
        securityPreview.textContent = `Código ${pedidoSalvo.codigo_seguranca}`;
      } else {
        securityPreview.textContent = 'Código de segurança não solicitado';
      }
    }

    carrinho = [];
    renderCarrinho();

    formulario.reset();
    atualizarTextoCodigoSeguranca();

    toast('Pedido cadastrado com sucesso!');

  } catch (erro) {
    console.error(erro);
    toast('Erro de conexão com o servidor.');
  }
});

renderCarrinho();
atualizarTextoCodigoSeguranca();