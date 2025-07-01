/*
  --------------------------------------------------------------------------------------
  Função para obter a lista de vinhos do servidor via GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = "http://127.0.0.1:5000/vinhos";
  fetch(url, {
    method: "get",
  })
    .then((response) => response.json())
    .then((data) => {
      data.vinhos.forEach((item) =>
        insertList(
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
        )
      );
    })
    .catch((error) => {
      console.error("Error:", error);
    });
};

/*
  --------------------------------------------------------------------------------------
  Limpa a tabela antes de recarregar os dados
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  var table = document.getElementById("myTable");
  while (table.rows.length > 1) {
    table.deleteRow(1);
  }
};

/*
  --------------------------------------------------------------------------------------
  Recarrega toda a tabela com dados atualizados
  --------------------------------------------------------------------------------------
*/
const refreshList = async () => {
  clearTable();
  await getList();
};

/*
  --------------------------------------------------------------------------------------
  Chama a função para carregar os dados quando a página estiver carregada
  --------------------------------------------------------------------------------------
*/
document.addEventListener("DOMContentLoaded", function () {
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
  const formData = new FormData();

  formData.append("fixed_acidity", fixed_acidity);
  formData.append("volatile_acidity", volatile_acidity);
  formData.append("citric_acid", citric_acid);
  formData.append("residual_sugar", residual_sugar);
  formData.append("chlorides", chlorides);
  formData.append("free_sulfur_dioxide", free_sulfur_dioxide);
  formData.append("total_sulfur_dioxide", total_sulfur_dioxide);
  formData.append("density", density);
  formData.append("pH", pH);
  formData.append("sulphates", sulphates);
  formData.append("alcohol", alcohol);

  let url = "http://127.0.0.1:5000/vinho";
  return fetch(url, {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        // tenta extrair mensagem de erro
        return response.json().then((err) => Promise.reject(err));
      }
      return response.json();
    })
    .catch((error) => {
      console.error("Error:", error);
      throw error;
    });
};

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
};

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
      const idItem = div.getElementsByTagName("td")[0].innerHTML;
      if (confirm("Você tem certeza que deseja remover este vinho?")) {
        div.remove();
        deleteItem(idItem);
      }
    };
  }
};

/*
  --------------------------------------------------------------------------------------
  Exclui um vinho do servidor via DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (id) => {
  let url = "http://127.0.0.1:5000/vinho?id=" + id;
  fetch(url, {
    method: "delete",
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error("Error:", error);
    });
};

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
  let free_sulfur_dioxide = document.getElementById(
    "newFreeSulfurDioxide"
  ).value;
  let total_sulfur_dioxide = document.getElementById(
    "newTotalSulfurDioxide"
  ).value;
  let density = document.getElementById("newDensity").value;
  let pH = document.getElementById("newPh").value;
  let sulphates = document.getElementById("newSulphates").value;
  let alcohol = document.getElementById("newAlcohol").value;

  // Validação básica
  if (
    !fixed_acidity ||
    !volatile_acidity ||
    !citric_acid ||
    !residual_sugar ||
    !chlorides ||
    !free_sulfur_dioxide ||
    !total_sulfur_dioxide ||
    !density ||
    !pH ||
    !sulphates ||
    !alcohol
  ) {
    alert("Todos os campos são obrigatórios!");
    return;
  }

  if (
    [
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
    ].some(isNaN)
  ) {
    alert("Todos os campos devem ser numéricos!");
    return;
  }

  try {
    const result = await postItem(
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
    );
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

    closeModal("register");

    document.getElementById("quality-result").textContent =
      "Qualidade prevista: " + judgeQuality(result.quality);
    showModal("result");
  } catch (error) {
    console.error(error);
    document.getElementById("quality-result").textContent ="Erro ao adicionar vinho. Tente novamente.";
    showModal("result");
  }
};

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
  var item = [
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
  ];
  var table = document.getElementById("myTable");
  var row = table.insertRow();

  // Adiciona todas as células
  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  // Qualidade
  var qualityCell = row.insertCell(item.length);
  qualityCell.textContent = judgeQuality(quality);

  // Botão de delete
  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);
  removeElement();
};

//Testes locais mais simples

function getRandom(min, max) {
  return (Math.random() * (max - min) + min).toFixed(3);
}

function fillTestData() {
  document.getElementById("newFixedAcidity").value = getRandom(4.6, 15.9);
  document.getElementById("newVolatileAcidity").value = getRandom(0.12, 1.58);
  document.getElementById("newCitricAcid").value = getRandom(0.0, 1.0);
  document.getElementById("newResidualSugar").value = getRandom(0.9, 15.5);
  document.getElementById("newChlorides").value = getRandom(0.012, 0.611);
  document.getElementById("newFreeSulfurDioxide").value = getRandom(1.0, 72.0);
  document.getElementById("newTotalSulfurDioxide").value = getRandom(
    6.0,
    289.0
  );
  document.getElementById("newDensity").value = getRandom(0.98711, 1.03898);
  document.getElementById("newPh").value = getRandom(2.74, 4.01);
  document.getElementById("newSulphates").value = getRandom(0.33, 2.0);
  document.getElementById("newAlcohol").value = getRandom(8.0, 14.9);
}

//Colocar categoria da qualidade

const judgeQuality = (quality) => {
  if (quality <= 5) {
    return "Baixa";
  }

  if (quality <= 7) {
    return "Média";
  }

  if (quality > 7) {
    return "Alta";
  }
};

//Funções para o modal

function closeModal(modalName) {
  const modal = document.getElementById(`${modalName}-modal`);
  if (modal) modal.style.display = "none";
}

function showModal(modalName) {
  const modal = document.getElementById(`${modalName}-modal`);
  if (modal) modal.style.display = "block";
  else console.error("Modal not found!");
}
