package com.skf.labs.fileupload;

import com.skf.labs.fileupload.storage.StorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

@Controller
public class FileUploadController {

  private final StorageService storageService;

  @Autowired
  public FileUploadController(StorageService storageService) {
    this.storageService = storageService;
  }

  @GetMapping("/")
  public String listUploadedFiles() {

    return "index";
  }

  @PostMapping("/")
  public String handleFileUpload(@RequestParam("file") MultipartFile file,
      Model model) {
    String[] allowedFileExtensions = new String[] { "txt", "pdf", "png", "jpg", "gif", "html" };
    String fileExtension = file.getOriginalFilename().substring(file.getOriginalFilename().lastIndexOf(".") + 1);
    if (java.util.Arrays.asList(allowedFileExtensions).contains(fileExtension)) {
      storageService.store(file);
      model.addAttribute("uploaded", "You successfully uploaded!");
      return "index";
    } else {
      model.addAttribute("uploaded", "File extension not allowed");
      return "index";
    }
  }
}
