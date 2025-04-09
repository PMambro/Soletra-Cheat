// static/js/app.js

function getWords() {
    const letters = document.getElementById('letters').value.trim();
    const required = document.getElementById('required').value.trim();
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';

    if (letters.length !== 7 || required.length !== 1) {
        alert("Enter exactly 7 letters and 1 required letter!");
        return;
    }

    fetch('/get_words', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letters: letters, required: required })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.grouped_words || Object.keys(data.grouped_words).length === 0) {
            resultDiv.textContent = "No matching words found.";
            return;
        }

        for (const [length, words] of Object.entries(data.grouped_words)) {
            const section = document.createElement('div');
            section.className = 'group';

            const title = document.createElement('h3');
            title.textContent = `Words with ${length} letters`;
            section.appendChild(title);

            words.forEach(word => {
                const span = document.createElement('span');
                span.className = 'word';
                span.textContent = word;
                section.appendChild(span);
            });

            resultDiv.appendChild(section);
        }
    })
    .catch(err => {
        console.error(err);
        alert("Error generating words.");
    });
}
