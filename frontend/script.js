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

    const responseText = await response.text();

    console.log("Raw backend response:", responseText);

    if (!response.ok) {
        throw new Error(
            `Server error ${response.status}: ${responseText}`
        );
    }

    const resultData = JSON.parse(responseText);

    console.log("Backend result:", resultData);

    // SHOW RESULT
    result.classList.remove("hidden");

    if (resultData.eligible) {
        eligibility.innerHTML = "✅ Eligible";
    } else {
        eligibility.innerHTML = "❌ Not Eligible";
    }

    emi.innerHTML =
        `₹${Number(resultData.emi).toLocaleString("en-IN")}`;

    creditDisplay.textContent =
        resultData.credit_score;

    employmentDisplay.textContent =
        resultData.employment;

    message.textContent =
        resultData.message;

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

    result.scrollIntoView({
        behavior: "smooth"
    });

} catch (error) {

    console.error("Connection error:", error);

    result.classList.remove("hidden");

    eligibility.innerHTML =
        "⚠️ Backend connection failed";

    emi.innerHTML =
        "API request failed.";

    message.textContent =
        error.message;

    tips.innerHTML = "";
}