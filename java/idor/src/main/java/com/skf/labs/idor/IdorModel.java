package com.skf.labs.idor;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import com.itextpdf.text.Document;
import com.itextpdf.text.pdf.PdfWriter;
import com.itextpdf.text.Font;
import com.itextpdf.text.Chunk;
import com.itextpdf.text.FontFactory;
import com.itextpdf.text.BaseColor;
import com.itextpdf.text.DocumentException;

public class IdorModel {

public static List<Integer> pdfs = new ArrayList<Integer>();
private static int min = 1;
private static int max = 100;
private static Random rand;

   public static void init(){
       createPdfPool();
   }

   public static void createPdfPool(){
    rand = new Random();
    for(int i = 0; i < 60; i++) createPdf("Try again!");
    createPdf("You have found the secret pdf, congratulations!");
    }

   public static int createPdf(String message){
    try{
       int pdfId = rand.nextInt(max-min+1)+min;
       Document document = new Document();
       PdfWriter.getInstance(document, new FileOutputStream(pdfId+".pdf"));
       document.open();
       Font font = FontFactory.getFont(FontFactory.COURIER, 16, BaseColor.BLACK);
       Chunk chunk = new Chunk(message, font);
       document.add(chunk);
       document.close();
       pdfs.add(pdfId);
       return pdfId;
    }catch(FileNotFoundException e){
        e.printStackTrace();
    }catch(DocumentException e){
        e.printStackTrace();
    }
    return -1;
   }  
}
