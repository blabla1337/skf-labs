package com.skf.labs.fileupload;

import com.skf.labs.fileupload.storage.StorageProperties;
import com.skf.labs.fileupload.storage.StorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.InputStreamResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;

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

  @GetMapping("/{filename}")
  @ResponseBody
  public  ResponseEntity<Resource> serveFile(@PathVariable String filename) throws IOException {
      Resource file = storageService.loadAsResource("../downloads/" + filename);
      return ResponseEntity.ok().header(HttpHeaders.CONTENT_TYPE, "image/png").body(file);
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
