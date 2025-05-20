document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const input = document.querySelector("input[name='message']");
  const output = document.querySelector("#chat-output");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const userMessage = input.value.trim();
    if (!userMessage) return;

    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.textContent = "You: " + userMessage;
    output.appendChild(userDiv);

    try {
      const response = await fetch("/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `message=${encodeURIComponent(userMessage)}`
      });

      const data = await response.json();
      const answerText = data.reply || "No response";

      const botDiv = document.createElement("div");
      botDiv.className = "message bot";
      botDiv.textContent = "Bot: " + answerText;
      output.appendChild(botDiv);
    } catch (error) {
      console.error("Xəta baş verdi:", error);
      const errorDiv = document.createElement("div");
      errorDiv.className = "message bot";
      errorDiv.textContent = "Bot: Bağışla, bir xəta baş verdi.";
      output.appendChild(errorDiv);
    }

    input.value = "";
  });
});
