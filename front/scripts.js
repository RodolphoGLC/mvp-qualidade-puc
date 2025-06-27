/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de vinhos do servidor via GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/vinhos';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.vinhos.forEach(item => insertList(
        item.id,
        item.fixed_acidity,
        item.volatile_acidity,
        item.citric_acid,
        item.residual_sugar,
        item.chlorides,
        item.free_sulfur_dioxide,
        item.total_sulfur_dioxide,
        item.density,
        item.pH,
        item.sulphates,
        item.alcohol,
        item.quality
      ));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Limpa a tabela antes de recarregar os dados
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  var table = document.getElementById('myTable');
  while(table.rows.length > 1) {
    table.deleteRow(1);
  }
}

/*
  --------------------------------------------------------------------------------------
  Recarrega toda a tabela com dados atualizados
  --------------------------------------------------------------------------------------
*/
const refreshList = async () => {
  clearTable();
  await getList();
}

/*
  --------------------------------------------------------------------------------------
  Chama a função para carregar os dados quando a página estiver carregada
  --------------------------------------------------------------------------------------
*/
document.addEventListener('DOMContentLoaded', function() {
  getList();
});


/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo vinho via POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (
  fixed_acidity,
  volatile_acidity,
  citric_acid,
  residual_sugar,
  chlorides,
  free_sulfur_dioxide,
  total_sulfur_dioxide,
  density,
  pH,
  sulphates,
  alcohol
) => {
  const payload = {
    fixed_acidity: Number(fixed_acidity),
    volatile_acidity: Number(volatile_acidity),
    citric_acid: Number(citric_acid),
    residual_sugar: Number(residual_sugar),
    chlorides: Number(chlorides),
    free_sulfur_dioxide: Number(free_sulfur_dioxide),
    total_sulfur_dioxide: Number(total_sulfur_dioxide),
    density: Number(density),
    pH: Number(pH),
    sulphates: Number(sulphates),
    alcohol: Number(alcohol),
  };

  let url = 'http://127.0.0.1:5000/vinho';
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })
    .then((response) => {
      if (!response.ok) {
        // tenta extrair mensagem de erro
        return response.json().then(err => Promise.reject(err));
      }
      return response.json();
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
}


/*
  --------------------------------------------------------------------------------------
  Insere botão de deletar para cada linha
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Remove linha e exclui o vinho do servidor
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  for (let i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const idItem = div.getElementsByTagName('td')[0].innerHTML;
      if (confirm("Você tem certeza?")) {
        div.remove();
        deleteItem(idItem);
        alert("Removido!");
      }
    };
  }
}

/*
  --------------------------------------------------------------------------------------
  Exclui um vinho do servidor via DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (id) => {
  let url = 'http://127.0.0.1:5000/vinho?id=' + id;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Adiciona um novo vinho à tabela e atualiza a tela
  --------------------------------------------------------------------------------------
*/
const newItem = async (event) => {
  event.preventDefault();

  let fixed_acidity = document.getElementById("newFixedAcidity").value;
  let volatile_acidity = document.getElementById("newVolatileAcidity").value;
  let citric_acid = document.getElementById("newCitricAcid").value;
  let residual_sugar = document.getElementById("newResidualSugar").value;
  let chlorides = document.getElementById("newChlorides").value;
  let free_sulfur_dioxide = document.getElementById("newFreeSulfurDioxide").value;
  let total_sulfur_dioxide = document.getElementById("newTotalSulfurDioxide").value;
  let density = document.getElementById("newDensity").value;
  let pH = document.getElementById("newPh").value;
  let sulphates = document.getElementById("newSulphates").value;
  let alcohol = document.getElementById("newAlcohol").value;

  // Validação básica
  if (!fixed_acidity || !volatile_acidity || !citric_acid || !residual_sugar || !chlorides || !free_sulfur_dioxide || !total_sulfur_dioxide || !density || !pH || !sulphates || !alcohol) {
    alert("Todos os campos são obrigatórios!");
    return;
  }

  if ([fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol].some(isNaN)) {
    alert("Todos os campos devem ser numéricos!");
    return;
  }

  try {
    const result = await postItem(fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol);
    // Limpa o formulário
    document.getElementById("newFixedAcidity").value = ""; 
    document.getElementById("newVolatileAcidity").value = ""; 
    document.getElementById("newCitricAcid").value = ""; 
    document.getElementById("newResidualSugar").value = ""; 
    document.getElementById("newChlorides").value = ""; 
    document.getElementById("newFreeSulfurDioxide").value = ""; 
    document.getElementById("newTotalSulfurDioxide").value = ""; 
    document.getElementById("newDensity").value = ""; 
    document.getElementById("newPh").value = ""; 
    document.getElementById("newSulphates").value = ""; 
    document.getElementById("newAlcohol").value = ""; 

    // Recarrega a tabela
    await refreshList();

    alert("Vinho adicionado com sucesso!\nQualidade prevista: " + result.quality);
    document.querySelector('.items').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (error) {
    console.error(error);
    alert("Erro ao adicionar vinho. Tente novamente.");
  }
}

/*
  --------------------------------------------------------------------------------------
  Insere dados de um vinho na tabela
  --------------------------------------------------------------------------------------
*/
const insertList = (
  id,
  fixed_acidity,
  volatile_acidity,
  citric_acid,
  residual_sugar,
  chlorides,
  free_sulfur_dioxide,
  total_sulfur_dioxide,
  density,
  pH,
  sulphates,
  alcohol,
  quality
) => {
  var item = [id, fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  // Adiciona todas as células
  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  // Qualidade
  var qualityCell = row.insertCell(item.length);
  qualityCell.textContent = quality;

  // Botão de delete
  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);
  removeElement();
}

//Testes locais mais simples

function fillTestData() {
  document.getElementById("newFixedAcidity").value = "7.2";
  document.getElementById("newVolatileAcidity").value = "0.33";
  document.getElementById("newCitricAcid").value = "0.33";
  document.getElementById("newResidualSugar").value = "1.7";
  document.getElementById("newChlorides").value = "0.061";
  document.getElementById("newFreeSulfurDioxide").value = "3.0";
  document.getElementById("newTotalSulfurDioxide").value = "13.0";
  document.getElementById("newDensity").value = "0.996";
  document.getElementById("newPh").value = "3.23";
  document.getElementById("newSulphates").value = "1.1";
  document.getElementById("newAlcohol").value = "10.0";
}