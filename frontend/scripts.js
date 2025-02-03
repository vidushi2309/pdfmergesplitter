async function splitPDF() {
    const fileInput = document.getElementById("splitFile");
    const pagesInput = document.getElementById("splitPages");
    const resultText = document.getElementById("splitResult");

    if (!fileInput.files.length || !pagesInput.value) {
        resultText.innerText = "Please select a file and enter page numbers.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("pages", pagesInput.value);

    const response = await fetch("http://127.0.0.1:8000/split-pdf/", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();

    // Trigger direct download instead of showing a link
    const fileResponse = await fetch(`http://127.0.0.1:8000${result.download_url}`);
    const blob = await fileResponse.blob();

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `split_${fileInput.files[0].name}`;  // Set the filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

async function mergePDFs() {
    const fileInput = document.getElementById("mergeFiles");
    const resultText = document.getElementById("mergeResult");

    if (!fileInput.files.length) {
        resultText.innerText = "Please select at least one file.";
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < fileInput.files.length; i++) {
        formData.append("files", fileInput.files[i]);
    }

    const response = await fetch("http://127.0.0.1:8000/merge-pdf/", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();

    // Trigger direct download instead of showing a link
    const fileResponse = await fetch(`http://127.0.0.1:8000${result.download_url}`);
    const blob = await fileResponse.blob();

    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "merged.pdf";  // Set the filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
