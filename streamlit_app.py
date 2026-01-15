function myFunction(lessonPlan) {
  // 📄 Open your Google Doc by ID
  var templateId = "1mJFVM8TiPce4kJ76P3NKuvn-NwRIZjYJzQt86rIRKJY";
  var doc = DocumentApp.openById(templateId);
  var body = doc.getBody();

  // 🔁 Utility: escape special regex characters in replacement text
  function escapeForReplaceText(str) {
    if (!str) return ""; // handle empty or null
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
  }

  // 📌 Replace top-level placeholders (headers) if present
  var topLevelFields = ["Teacher", "Year/Class", "Subject", "Unit/Topic", "Week number", "Date"];
  topLevelFields.forEach(function(field) {
    if (lessonPlan[field]) {
      body.replaceText("\\{\\{" + field + "\\}\\}", escapeForReplaceText(lessonPlan[field]));
    }
  });

  // 🔁 Replace class placeholders dynamically
  if (lessonPlan.Classes) {
    for (var classKey in lessonPlan.Classes) {
      var classObj = lessonPlan.Classes[classKey];
      for (var placeholder in classObj) {
        if (classObj[placeholder]) { // ignore empty fields
          body.replaceText(
            "\\{\\{" + placeholder + "\\}\\}",
            escapeForReplaceText(classObj[placeholder])
          );
        }
      }
    }
  }

  // 📌 Save and close the document
  doc.saveAndClose();
}
