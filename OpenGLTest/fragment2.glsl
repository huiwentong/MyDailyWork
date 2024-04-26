#version 330 core
//const vec3 lightColor = vec3(0.8, 0.8, 0.8);
//const vec3 lightPosition = vec3(5.0, 7.0, 2.0);
//const vec3 viewPos = vec3(0, 0, 2);

in vec4 vertexColor;
in vec2 vTexCoord;
in vec3 FragPos;
in vec3 FragNormals;

uniform sampler2D uSampler;

uniform vec3 lightPosition;
uniform vec3 lightColor;
uniform vec3 viewPos;


out vec4 FragColor;


void main()
{
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * lightColor;


    vec3 normal = normalize(FragNormals);
    vec3 lightDir = normalize(lightPosition - FragPos);

    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = lightColor * diff;

    float specStrength = 1;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = lightColor * spec * specStrength;

    vec3 result = (ambient + specular + diffuse) * vec3(texture(uSampler, vTexCoord));
    FragColor = vec4(result, 1.0);

//    FragColor = vec4(texture(uSampler, vTexCoord)) * vec4(vertexColor);
//    FragColor = vec4(vertexColor);
}