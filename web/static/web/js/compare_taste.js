document.addEventListener("DOMContentLoaded", () => {
  const messageTag = document.querySelector(".subtitle");

  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = () => {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status !== 200) {
        messageTag.innerHTML = "Произошла непредвиденная ошибка. Пожалуйста, попробуйте заново.";
        messageTag.classList.add("has-text-danger-50");
      } else {
        const response = JSON.parse(xhr.responseText);
        messageTag.innerHTML = `Ваши музыкальные вкусы совпадают на <b>${response.result}%</b>!`;
      }
      document.querySelector(".loader").classList.add("is-hidden");
    }
  };
  xhr.open("GET", `/api/compare/${compared_to_username}`, true);
  xhr.send();
});