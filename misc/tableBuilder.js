const ROOT = document.getElementById("root")
let HEIGHT = document.getElementById("height").value
let WIDTH = document.getElementById("width").value

const CELL_WIDTH = 17
const CELL_HEIGHT = 17

const WALL = "wall"
const PATH = "path"

const handleTableChange = () => {
  WIDTH = document.getElementById("width").value
  HEIGHT = document.getElementById("height").value
  HEIGHT = HEIGHT > 3 ? HEIGHT : 3
  WIDTH = WIDTH > 3 ? WIDTH : 3
  redrawTable()
}

const getCell = (x, y) => {
  return document.getElementById(`${x}_${y}`)
}

const redrawTable = () => {
  ROOT.innerHTML = ""
  const table = document.createElement("table")
  table.className = "centered-block"
  ROOT.appendChild(table)

  for (let h = 0; h < HEIGHT; h++) {

    const row = document.createElement("tr")
    table.appendChild(row)

    for (let w = 0; w < WIDTH; w++) {
      const cell = document.createElement("td")
      row.appendChild(cell)
      cell.style.border = "solid orange 1px"
      cell.style.width = `${CELL_WIDTH}px`
      cell.style.height = `${CELL_HEIGHT}px`
      cell.className = WALL
      cell.id = `${w}_${h}`

      cell.addEventListener("click", (event) => {
        cell.className = cell.className === PATH ? WALL : PATH
      })
    }
  }
}

const getResult = () => {
  let result = ""
  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      result += getCell(x, y).className === WALL ? "█" : " "
    }
    result += "\n"
  }
  return result
}

const download = () => {
  const file = new Blob([ getResult() ], { type: "text/plain" })
  const a = document.createElement("a")
  a.target = "_BLANK"
  a.href = URL.createObjectURL(file)
  a.download = `maze_${WIDTH}x${HEIGHT}.txt`
  a.click()
}

redrawTable()