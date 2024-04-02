const rows = 30;
const cols = 50;
let grid = createEmptyGrid(rows, cols);
let intervalId;

var mode_start = true;

function createEmptyGrid(rows, cols) {
  let grid = new Array(rows);
  for (let i = 0; i < rows; i++) {
    grid[i] = new Array(cols).fill(0);
  }
  return grid;
}

function createRandomGrid(rows, cols) {
  let grid = new Array(rows);
  for (let i = 0; i < rows; i++) {
    grid[i] = new Array(cols).fill(0).map(() => (Math.random() > 0.7 ? 1 : 0));
  }
  return grid;
}

function updateGrid() {
  let newGrid = createEmptyGrid(rows, cols);
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      let neighbors = countNeighbors(i, j);
      if (grid[i][j] === 1) {
        newGrid[i][j] = neighbors === 2 || neighbors === 3 ? 1 : 0;
      } else {
        newGrid[i][j] = neighbors === 3 ? 1 : 0;
      }
    }
  }
  grid = newGrid;
  renderGrid();
}

function countNeighbors(row, col) {
  let count = 0;
  for (let i = row - 1; i <= row + 1; i++) {
    for (let j = col - 1; j <= col + 1; j++) {
      if (
        i >= 0 &&
        i < rows &&
        j >= 0 &&
        j < cols &&
        !(i === row && j === col)
      ) {
        count += grid[i][j];
      }
    }
  }
  return count;
}

function renderGrid() {
  let table = document.getElementById("grid");
  table.innerHTML = "";
  for (let i = 0; i < rows; i++) {
    let row = document.createElement("tr");
    for (let j = 0; j < cols; j++) {
      let cell = document.createElement("td");
      cell.addEventListener("click", (e) => {
        grid[i][j] = grid[i][j] == 1 ? 0 : 1;
        renderGrid();
      });
      cell.className = grid[i][j] === 1 ? "alive" : "";
      row.appendChild(cell);
    }
    table.appendChild(row);
  }
}

function startGame() {
  if (mode_start) {
    intervalId = setInterval(updateGrid, 100);
    document.getElementById("start").innerHTML = "stop";
    document.getElementById("start").style.backgroundColor = "red";
    mode_start = false;
  } else {
    document.getElementById("start").innerHTML = "start";
    document.getElementById("start").style.backgroundColor = "black";
    stopGame();
    mode_start = true;
  }
}
function stopGame() {
  clearInterval(intervalId);
  intervalId = null;
}
function clearGrid() {
  grid = createEmptyGrid(rows, cols);
  renderGrid();
}
grid = createEmptyGrid(rows, cols);
renderGrid();
