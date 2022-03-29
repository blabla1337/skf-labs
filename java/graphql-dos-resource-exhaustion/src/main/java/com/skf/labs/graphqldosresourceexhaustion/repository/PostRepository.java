package com.skf.labs.graphqldosresourceexhaustion.repository;
import com.skf.labs.graphqldosresourceexhaustion.entity.Post;

import org.springframework.data.jpa.repository.JpaRepository;


public interface PostRepository extends JpaRepository<Post,Integer>{
    
}
