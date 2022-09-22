const userCardTemplate = document.querySelector("[data-user-template]");
const dataUserCadsContainer = document.querySelector(
  "[data-user-cards-container]"
);
const searchInput = document.querySelector("[data-search]");

let user = [];

searchInput.addEventListener("input", (e) => {
  const value = e.target.value.toLowerCase(); 
  // this is because you do not want case sensitivity

  user.forEach(user => {
    // this will return true if the input value is found either in the email or the name of the user
    const isVisible = user.name.includes(value) || user.email.includes(value);
    user.element.classList.toggle("hide", !isVisible);
    // this toggle function let's us pass a name of a class in this case hide and a boolean
    // that tells it if its is so post to be on or off
  });
});

fetch("https://jsonplaceholder.typicode.com/users")
  .then((res) => res.json())
  .then((data) => {
    user = data.map(user => {
      const card = userCardTemplate.content.cloneNode(true).children[0];
      // this will clone the content iof the user card
      // this will return a document fragment
      const header = card.querySelector("[data-header");
      const body = card.querySelector(["[data-body]"]);
      header.textContent = user.name;
      body.textContent = user.email;
      dataUserCadsContainer.append(card);
      return { name: user.name, email: user.email, element: card };
    });
  });
