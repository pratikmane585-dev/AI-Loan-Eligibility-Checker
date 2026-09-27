const form = document.getElementById("loanForm");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const result = document.getElementById("result");
    const eligibility = document.getElementById("eligibility");
    const emi = document.getElementById("emi");
    const message = document.getElementById("message");
    const tips = document.getElementById("tips");

    const creditDisplay = document.getElementById("creditDisplay");
    const employmentDisplay = document.getElementById("employmentDisplay");

    const data = {
        name: document.getElementById("name").value,
        age: Number(document.getElementById("age").value),
        income: Number(document.getElementById("income").value),
        creditScore: Number(document.getElementById("creditScore").value),
        employment: document.getElementById("employment").value,
        loanAmount: Number(document.getElementById("loanAmount").value),
        tenure: Number(document.getElementById("tenure").value)
    };

    console.log("Sending data:", data);

    try {

        const response = await fetch(
          "https://ai-loan-eligibility-checker-297b.onrender.com/api/check-loan",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        console.log("Response status:", response.status);

        const resultData = await response.json();

        console.log("Backend result:", resultData);

        // SHOW RESULT
        result.classList.remove("hidden");

        // Eligibility
        if (resultData.eligible) {

            eligibility.innerHTML =
                "✅ Eligible";

        } else {

            eligibility.innerHTML =
                "❌ Not Eligible";
        }

        // EMI
        emi.innerHTML =
            `₹${Number(resultData.emi).toLocaleString("en-IN")}`;

        // Credit Score
        creditDisplay.textContent =
            resultData.credit_score;

        // Employment
        employmentDisplay.textContent =
            resultData.employment;

        // Message
        message.textContent =
            resultData.message;

        // Tips
        if (resultData.tips && resultData.tips.length > 0) {

            tips.innerHTML = `
                <ul>
                    ${resultData.tips
                        .map(tip => `<li>${tip}</li>`)
                        .join("")}
                </ul>
            `;

        } else {

            tips.innerHTML =
                "<p>No additional tips available.</p>";
        }

        // Scroll to result
        result.scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {

        console.error("Connection error:", error);

        result.classList.remove("hidden");

        eligibility.innerHTML =
            "⚠️ Backend connection failed";

        emi.innerHTML =
            "Please make sure Flask is running.";

        message.textContent =
            error.message;

        tips.innerHTML = "";
    }

});