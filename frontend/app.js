let token = "";

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${username}&password=${password}`
    });

    const data = await response.json();
    if (response.ok) {
        token = data.access_token;
        document.getElementById("token-status").textContent = "Zalogowano!";
    } else {
        document.getElementById("token-status").textContent = "Błąd logowania";
    }
}

async function exportData() {
    const collection = document.getElementById("collection-export").value;
    const format = document.getElementById("format-export").value;

    const response = await fetch(`/export/${collection}?format=${format}`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = `export.${format}`;
    a.click();
}

async function importData() {
    const collection = document.getElementById("collection-import").value;
    const file = document.getElementById("import-file").files[0];

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`/import/${collection}`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData
    });

    const result = await response.json();
    alert(`Zaimportowano: ${result.imported} rekordów`);
}

async function fetchExternal() {
    const response = await fetch("/external/fetch");
    const data = await response.json();
    document.getElementById("external-data").textContent = JSON.stringify(data, null, 2);
}
