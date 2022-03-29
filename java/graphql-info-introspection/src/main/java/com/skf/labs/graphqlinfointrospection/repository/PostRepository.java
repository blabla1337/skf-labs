package com.skf.labs.graphqlinfointrospection.repository;
import com.skf.labs.graphqlinfointrospection.entity.Post;

import org.springframework.data.jpa.repository.JpaRepository;


public interface PostRepository extends JpaRepository<Post,Integer>{
    
}
