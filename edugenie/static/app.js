async function sendRequest(endpoint, inputId, resultId) {

    const input = document.getElementById(inputId);
    const result = document.getElementById(resultId);

    const text = input.value.trim();

    if (!text) {
        result.innerHTML = "Please enter some text.";
        return;
    }

    result.innerHTML = "EduGenie is thinking...";

    try {

        const response = await fetch(endpoint, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Request failed."
            );
        }

        let heading = "";

        if (resultId === "qa-result") {
            heading = "<strong>Answer:</strong><br><br>";
        }

        if (resultId === "explain-result") {
            heading = "<strong>Explanation:</strong><br><br>";
        }

        if (resultId === "summary-result") {
            heading = "<strong>Summary:</strong><br><br>";
        }

        result.innerHTML =
            heading + formatText(data.result);

    } catch (error) {

        result.innerHTML =
            "Error: " + error.message;
    }
}


/* Text formatting */

function formatText(text) {

    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replaceAll("\n\n", "<br><br>")
        .replaceAll("\n", "<br>");
}


/* Ask */

document
    .getElementById("qa-form")
    .addEventListener("submit", function(event) {

        event.preventDefault();

        sendRequest(
            "/qa",
            "qa-input",
            "qa-result"
        );

    });


/* Explain */

document
    .getElementById("explain-form")
    .addEventListener("submit", function(event) {

        event.preventDefault();

        sendRequest(
            "/explain",
            "explain-input",
            "explain-result"
        );

    });


/* Summary */

document
    .getElementById("summary-form")
    .addEventListener("submit", function(event) {

        event.preventDefault();

        sendRequest(
            "/summarize",
            "summary-input",
            "summary-result"
        );

    });


/* Quiz */

document
    .getElementById("quiz-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const input =
            document.getElementById("quiz-input");

        const result =
            document.getElementById("quiz-result");

        const text = input.value.trim();

        if (!text) {

            result.innerHTML =
                "Please enter a topic.";

            return;
        }

        result.innerHTML =
            "Generating quiz...";

        try {

            const response = await fetch(
                "/quiz",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Quiz generation failed."
                );
            }

            renderQuiz(data, result);

        } catch (error) {

            result.innerHTML =
                "Error: " + error.message;
        }

    });


function renderQuiz(data, result) {

    let html =
        "<strong>Quiz:</strong><br><br>";

    data.questions.forEach(function(question, index) {

        html += `
            <div class="quiz-question">

                <strong>
                    Q${index + 1}:
                    ${escapeHtml(question.question)}
                </strong>
        `;

        question.options.forEach(function(option) {

            html += `
                <label class="option">

                    <input
                        type="radio"
                        name="question-${index}"
                        value="${escapeHtml(option)}"
                    >

                    ${escapeHtml(option)}

                </label>
            `;

        });

        html += `
                <button
                    type="button"
                    class="check-question"
                    data-index="${index}"
                >
                    Check Answer
                </button>

                <div
                    id="feedback-${index}"
                ></div>

            </div>
        `;

    });

    result.innerHTML = html;

    result
        .querySelectorAll(".check-question")
        .forEach(function(button) {

            button.addEventListener(
                "click",
                function() {

                    const index =
                        Number(button.dataset.index);

                    const question =
                        data.questions[index];

                    const selected =
                        result.querySelector(
                            `input[name="question-${index}"]:checked`
                        );

                    const feedback =
                        document.getElementById(
                            `feedback-${index}`
                        );

                    if (!selected) {

                        feedback.innerHTML =
                            "<p>Please select an answer.</p>";

                        return;
                    }

                    if (
                        selected.value ===
                        question.correct_answer
                    ) {

                        feedback.innerHTML =
                            "<p><strong>✔ Correct!</strong></p>";

                    } else {

                        feedback.innerHTML = `
                            <p>
                                ❌ Incorrect.
                                Correct answer:
                                <strong>
                                    ${escapeHtml(
                                        question.correct_answer
                                    )}
                                </strong>
                            </p>
                        `;
                    }

                }
            );

        });
}


/* Learning Path */

document
    .getElementById("learning-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const input =
            document.getElementById("learning-input");

        const result =
            document.getElementById("learning-result");

        const topic =
            input.value.trim();

        if (!topic) {

            result.innerHTML =
                "Please enter a topic.";

            return;
        }

        result.innerHTML =
            "Building your learning path...";

        try {

            const response = await fetch(
                "/learn/recommendations",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        topic: topic,

                        level: "beginner",

                        weekly_hours: 5

                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Learning path failed."
                );
            }

            renderLearningPath(
                data,
                result
            );

        } catch (error) {

            result.innerHTML =
                "Error: " + error.message;
        }

    });


function renderLearningPath(data, result) {

    let html = `
        <strong>
            Learning Recommendations:
        </strong>

        <br><br>

        <h3>
            ${escapeHtml(data.topic)}
            Learning Path
        </h3>

        <p>
            Level:
            <strong>
                ${escapeHtml(data.level)}
            </strong>
        </p>
    `;

    data.steps.forEach(function(step) {

        html += `
            <div class="path">

                <h3>
                    ${escapeHtml(step.stage)}
                </h3>

                <p>
                    Estimated:
                    ${step.estimated_weeks}
                    week(s)
                </p>

                <ul>
        `;

        step.topics.forEach(function(topic) {

            html += `
                <li>
                    ${escapeHtml(topic)}
                </li>
            `;

        });

        html += `
                </ul>
        `;

        if (
            step.resources &&
            step.resources.length
        ) {

            html += "<h4>Resources</h4>";

            step.resources.forEach(function(resource) {

                if (resource.url) {

                    html += `
                        <p>
                            <a
                                href="${escapeHtml(resource.url)}"
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                ${escapeHtml(resource.title)}
                            </a>
                            -
                            ${escapeHtml(resource.why)}
                        </p>
                    `;

                } else {

                    html += `
                        <p>
                            ${escapeHtml(resource.title)}
                            -
                            ${escapeHtml(resource.why)}
                        </p>
                    `;
                }

            });
        }

        html += "</div>";

    });

    result.innerHTML = html;
}


/* Escape HTML */

function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}