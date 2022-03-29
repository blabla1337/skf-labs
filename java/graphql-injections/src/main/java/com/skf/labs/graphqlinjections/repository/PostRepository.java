package com.skf.labs.graphqlinjections.repository;
import com.skf.labs.graphqlinjections.entity.Post;

import org.springframework.data.jpa.repository.JpaRepository;


public interface PostRepository extends JpaRepository<Post,Integer>{
    
}
