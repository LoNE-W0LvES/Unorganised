function displayColors(event) {
  event.preventDefault();
  const colorValues = {};
  const form = event.target;
  colorValues["mode"] = colorSelect.value;
  if (colorSelect.value === "Custom") {
    for (const input of form.elements) {
      if (input.type === "color") {
        colorValues[input.name] = input.value;
      }
    }
  }
  if (colorSelect.value === "Static") {
    colorValues["image"] = colorPickX.value;
  }
  const query = new URLSearchParams(colorValues).toString();
  console.log(colorSelect.value);
  window.location.href = `display_values.html?${query}`;
}

const images = document.querySelectorAll(".image");
const colorSelect = document.getElementById("colors");
const colorPickers = document.querySelectorAll(".color-picker");
const colorPickX = document.getElementById("color-picker0");

window.onload = function(){
  const name = [
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000",
    "#ff0000"
  ];
  const base64Index = [0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1];
  const base64Image = [
    "data:image/png;base64,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",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIgAAAD/AgMAAABX83a4AAAADFBMVEXO1NuXprQqLzNIYHm3cs7dAAAAAnRSTlMBtzqN2lYAAAROSURBVHgB7Zq5kuM2EIZ7T2U+noCPsnS0qW+H8yh8n0bVMBdXhs/ct8PNEXAcUAk0QNtdDYIiG1zJ98WebPAB9bF5FP6CAMcyHss1IS3NyheQj+dILCC0KI2YI5zXA9pr5CuYVeMUYus5UkWFBJjXjhQyACxk3AJps0qW8RnRKkkmI0pFyYBSUZ0BpaJkRiSraBlQKkpGENIquTMJsT9BoZorED8hhoZLq5g+lFwimoy0jmqN7E7Y+hEh3Trpi82rWNcORRVyCWnJY9AqxAMZ6VHL7CIaigmxN7EgUzkkooSEHTkzaBVjn5NjBM3wgPYmFLoSHpBnBO1X8CyirdV9bgdooiA1VCcGlcpXUBEjfL0FmWZvbM0DCLwcADlDH5zXR4SsxzIgl9tEpHmxigyANO31iHdzIrIKsAxgSP7dqTsvZBVgGbDD+Jw6nFUXZMBD6vwzj4u647ksA1Tnz8m8UqMqgpCaqZA0d5eRB2WEB+DFGnJIAwSHNcRm5A9Y5X/gsrlsLpvL5rK5bC6by/3lVcLqKnUauLzFIRj3Qye9lxpXsW/PA1Ou9juZG6Eb5hkwl72XuQ5uj2kvjkso1DIXkMa9eLxFl2uPaD+RuWmnWnlJwjb/eWwHmQusJbFgXlFSbeVk18zLGbvcEiPJXEBzqIFVjm/Oihzat3kur9J+ApXOCo3nf+2iIAOwytsqCZvAKozgkVUOhbwX6mYvCD2PaEpJ2H5JOdlEuXQl8zJmxKnwIzI0BTHHV65ljHUJMVY6qWUygq1bScKdH5HOS1e0zBRQ4xVJWKtIqpmQdrgUc/GKmGtDGZl07YnqYhK2LiM6Wcpje5e7G103FJMw4YhwdCuq5CRs9Z1OKrTPSGQZHcrtSy+ICRzRB61i6DlhjrmIQavcBh5IMbfxxtZKhV8Nn2OuZ1CpfMUD/DZyzOUpWqXmAUYGeQjnMg9+UTnKAPBy7KZfe4m5jLAnVNynefFc4AEwEnP9EulZRT5BoskN6PG89n2QAQf01doXc0gDYOuV726aW8XVmCvt5gG4F+TREhn79GRC/Ary4BWrHBRyWl/lxfWr+H/QKieNXFwlXHY5/EOu6Ld39x/Qlz/4iv5BfdFP3fYebe/R9h5t79H/6j26/wNcrtoo0ep2KyH+FZu279Lcaeu3rDEiI5hjUjFeJ2G2dem0pVJ7zD3mPea4mV0eyPQSAisvJz+ssjj5uUlRsjnbWEs6z/WE99E1qyBwA3i5Th/45r03yzSucODLMpVPSZhVgoo+LNPkwLESc8NbY8ylG0kKWuZHn5ONqGgZ6nMSFhUtQzmrkahomQmJWoVl9mhxSsKiomQ6l5E7UVHxx/yaA19D5dPc87Bs3/5tSfjBLHJ3x5JuzC5cVL7oc8RecVY+rKlkxFxxbh9qrbJA7OXfECiZrJIRc9Qqc0R3pvIKad9eqPQaGRYqTiEmLGPuxZ+CxN+GdDOizyr4M8Y0MYB1NsC/AAAAAElFTkSuQmCC",
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAACzBAMAAADxkbgpAAAAD1BMVEVHcEyWpbNJYXspLC81R1r/X/dbAAAAAnRSTlMAlm//+0kAAAC3SURBVHgB7ZbHrQMxDAX5K3CowPvw7vaGAgSK/be0OUk/58ShToMReKUoLSHexJhxE0U/3J4NqtgBDFUhO+5g9xVfoviplXzyRjDc26jhfnVfvb/62o33KmQKfYXTjvNYZfAiqqkZPlpGELM65SZNvK/qe6r+cuXKlStXrly5ivcU71eITZ3MTdTuHadAYtT6CglkX532ADYo2XEeq2OiwPvK/nLlVXHaAfL+caoXIdW2oQ2VZYQOoX7h0SJvY58AAAAASUVORK5CYII="
  ];
  images.forEach(function (image, index) {
    image.style.backgroundColor = name[index];
    image.src = base64Image[base64Index[index]];
  });
  colorPickers.forEach(function (colorPicker, index) {
  colorPicker.value = name[index];
  });
};

colorSelect.addEventListener("change", function () {
  images.forEach(function (image, index) {
    colorPickers[index].style.visibility = "visible";
    image.addEventListener("click", function () {
      if (colorSelect.value === "Custom") {
        colorPickers[index].click(); 
        colorPickers[index].addEventListener("input", () => {
          image.style.backgroundColor = colorPickers[index].value;
        });
      }
      if (colorSelect.value === "Static") {
        colorPickX.click();
        colorPickX.addEventListener("input", () => {
          images.forEach(function (img) {
            img.style.backgroundColor = colorPickX.value;
          });
        });
      }
    });
  });
});