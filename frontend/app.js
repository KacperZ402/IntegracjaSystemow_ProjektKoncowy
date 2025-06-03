let token = "";

document.addEventListener("DOMContentLoaded", () => {
    token = localStorage.getItem("token");
    const user = localStorage.getItem("user");

    if (!token) {
        window.location.href = "/login";
    } else {
        const userNameEl = document.getElementById("user-name");
        if (userNameEl) {
            userNameEl.textContent = user || "użytkowniku";
        }
    }
});

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login";
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

async function generateReport() {
    const year = document.getElementById("report-year").value;
    const response = await fetch(`/report?year=${year}`);
    const data = await response.json();
    document.getElementById("report-output").textContent = JSON.stringify(data, null, 2);
}

async function checkCorrelation() {
    const response = await fetch("/correlation");
    const data = await response.json();
    document.getElementById("correlation-output").textContent = JSON.stringify(data, null, 2);
}

async function drawChart(year) {
    const res = await fetch(`/report?year=${year}`);
    const data = await res.json();

    const sectors = data.details.industrial.map(i => i.sector);
    const industrial = data.details.industrial.map(i => i.value_mln_pln);
    const emissions = data.details.emissions.map(e => e.amount_tonnes);
    const wastewater = data.details.wastewater.map(w => w.volume_hm3);

    const ctx = document.getElementById("myChart").getContext("2d");

    if (window.myChart && typeof window.myChart.destroy === "function") {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: sectors,
            datasets: [
                {
                    label: "Produkcja (mln PLN)",
                    data: industrial,
                    backgroundColor: "rgba(75, 192, 192, 0.6)"
                },
                {
                    label: "Emisje (tony)",
                    data: emissions,
                    backgroundColor: "rgba(255, 99, 132, 0.6)"
                },
                {
                    label: "Ścieki (hm³)",
                    data: wastewater,
                    backgroundColor: "rgba(54, 162, 235, 0.6)"
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
