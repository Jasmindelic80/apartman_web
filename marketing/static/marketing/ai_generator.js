// marketing/static/marketing/ai_generator.js
// AI Generator za društvene mreže - dugme u Django adminu

document.addEventListener('DOMContentLoaded', function() {
    const tekstField = document.querySelector('#id_tekst');
    if (!tekstField) return;

    // Kreiraj UI iznad textarea
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'background:#fff9eb;padding:1rem;margin:1rem 0;border-left:4px solid #c9a84c';
    wrapper.innerHTML = `
        <h3 style="margin:0 0 1rem;color:#1a1a2e;font-size:1rem">🤖 AI Generator posta</h3>

        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem">
            <select id="ai-tip" style="padding:0.5rem;border:1px solid #ddd">
                <option value="opci">📝 Opći post</option>
                <option value="ponuda">💰 Posebna ponuda</option>
                <option value="izlet">🗺️ Izlet/atrakcija</option>
                <option value="restoran">🍽️ Restoran/kuhinja</option>
                <option value="sezona">🌸 Sezonski post</option>
            </select>

            <select id="ai-jezik" style="padding:0.5rem;border:1px solid #ddd">
                <option value="bs">🇧🇦 Bosanski</option>
                <option value="en">🇬🇧 English</option>
                <option value="de">🇩🇪 Deutsch</option>
                <option value="it">🇮🇹 Italiano</option>
            </select>

            <input type="text" id="ai-tema" placeholder="Tema (opciono): npr. Štrbački buk"
                   style="padding:0.5rem;border:1px solid #ddd;flex:1;min-width:200px">

            <button type="button" id="ai-generiraj"
                    style="background:#c9a84c;color:#1a1a2e;border:none;padding:0.5rem 1.5rem;cursor:pointer;font-weight:600">
                ✨ Generiraj
            </button>
        </div>

        <div id="ai-status" style="font-size:0.85rem;color:#666;display:none"></div>
    `;

    tekstField.parentNode.insertBefore(wrapper, tekstField);

    // Generiraj klik
    document.getElementById('ai-generiraj').addEventListener('click', async function() {
        const status = document.getElementById('ai-status');
        const platforma = document.querySelector('#id_platforma').value;
        const tip = document.getElementById('ai-tip').value;
        const jezik = document.getElementById('ai-jezik').value;
        const tema = document.getElementById('ai-tema').value;

        status.style.display = 'block';
        status.style.color = '#666';
        status.textContent = '⏳ Generiram post...';

        try {
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch('/marketing/ai-generator/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body: JSON.stringify({ tip, platforma, jezik, tema }),
            });

            const data = await response.json();

            if (data.error) {
                status.style.color = '#ef4444';
                status.textContent = '❌ Greška: ' + data.error;
                return;
            }

            // Popuni tekst i hashtagove
            document.querySelector('#id_tekst').value = data.tekst;
            const hashtagField = document.querySelector('#id_hashtagovi');
            if (hashtagField && data.hashtagovi) {
                hashtagField.value = data.hashtagovi;
            }

            status.style.color = '#10b981';
            status.textContent = '✅ Post generiran! Pregledaj i sačuvaj.';
        } catch (err) {
            status.style.color = '#ef4444';
            status.textContent = '❌ Greška: ' + err.message;
        }
    });
});
