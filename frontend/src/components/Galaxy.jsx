import React, { useRef, useEffect } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer";

export default function Galaxy({ stars = [], fetchPlanetsForStar, isFullscreen = false, onRequestExit }) {
  const mountRef = useRef(null);
  const focusedStarRef = useRef(null);
  const focusedLabelRef = useRef(null);
  const planetLabelsRef = useRef([]); // Store all planet labels
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const controlsRef = useRef(null);

  useEffect(() => {
    const currentMount = mountRef.current;
    if (!currentMount || stars.length === 0) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x01010f);
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(
      75,
      currentMount.clientWidth / currentMount.clientHeight,
      0.1,
      200000
    );
    const initialCameraPosition = new THREE.Vector3(0, 200, 1200);
    camera.position.copy(initialCameraPosition);
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    currentMount.appendChild(renderer.domElement);

    // Label renderer
    const labelRenderer = new CSS2DRenderer();
    labelRenderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
    labelRenderer.domElement.style.position = "absolute";
    labelRenderer.domElement.style.top = "0px";
    labelRenderer.domElement.style.pointerEvents = "none";
    currentMount.appendChild(labelRenderer.domElement);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 10;
    controls.maxDistance = 80000;
    controls.target.set(0, 0, 0);
    controlsRef.current = controls;

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const mainLight = new THREE.PointLight(0xffffff, 1.5, 0, 2);
    mainLight.position.set(500, 1500, 500);
    scene.add(mainLight);

    const focusLight = new THREE.PointLight(0xffffff, 3, 5000);
    focusLight.visible = false;
    scene.add(focusLight);

    // Starfield background
    const starfieldGeom = new THREE.BufferGeometry();
    const starfieldCount = 10000;
    const starfieldPositions = new Float32Array(starfieldCount * 3);
    for (let i = 0; i < starfieldCount * 3; i++) {
      starfieldPositions[i] = (Math.random() - 0.5) * 100000;
    }
    starfieldGeom.setAttribute("position", new THREE.BufferAttribute(starfieldPositions, 3));
    const starfieldMat = new THREE.PointsMaterial({ 
      color: 0xffffff, 
      size: 10, 
      sizeAttenuation: true, 
      transparent: true, 
      opacity: 0.8 
    });
    const starfield = new THREE.Points(starfieldGeom, starfieldMat);
    scene.add(starfield);

    // Helper: convert RA/Dec to 3D
    const raDecTo3D = (ra, dec, dist) => {
      const raRad = THREE.MathUtils.degToRad(ra);
      const decRad = THREE.MathUtils.degToRad(dec);
      const r = (dist ? Math.log(dist + 1) : 10) * 200;
      return {
        x: r * Math.cos(decRad) * Math.cos(raRad),
        y: r * Math.sin(decRad),
        z: r * Math.cos(decRad) * Math.sin(raRad)
      };
    };

    const starGroup = new THREE.Group();
    const planetGroup = new THREE.Group();
    const focusGroup = new THREE.Group();
    scene.add(starGroup, planetGroup, focusGroup);

    // Add stars
    stars.forEach(star => {
      if (star.ra == null || star.dec == null) return;
      const { x, y, z } = raDecTo3D(star.ra, star.dec, star.sy_dist);
      const radius = star.star_radius ? Math.max(Math.log(star.star_radius + 1), 1) : 2;

      const geom = new THREE.SphereGeometry(radius, 24, 24);
      const mat = new THREE.MeshPhongMaterial({ 
        emissive: 0xffee88, 
        color: 0xffffcc, 
        shininess: 100
      });
      const mesh = new THREE.Mesh(geom, mat);
      mesh.position.set(x, y, z);
      mesh.userData.starData = star;
      mesh.userData.originalRadius = radius;
      mesh.userData.originalPosition = new THREE.Vector3(x, y, z);

      // Star label (hidden by default)
      const div = document.createElement("div");
      div.className = "label";
      div.textContent = star.name || "Star";
      div.style.color = "#fff";
      div.style.fontSize = "14px";
      div.style.padding = "4px 8px";
      div.style.background = "rgba(0,0,0,0.7)";
      div.style.borderRadius = "4px";
      div.style.fontWeight = "bold";
      div.style.pointerEvents = "none";
      const label = new CSS2DObject(div);
      label.position.set(0, radius * 2, 0);
      label.visible = false;
      mesh.add(label);
      mesh.userData.label = label;

      starGroup.add(mesh);
    });

    // Helper to clear a group
    const clearGroup = (group) => {
      while (group.children.length > 0) {
        const obj = group.children[0];
        group.remove(obj);
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) obj.material.dispose();
      }
    };

    const resetView = () => {
      // Remove focused label
      if (focusedLabelRef.current && focusedLabelRef.current.parent) {
        focusedLabelRef.current.parent.remove(focusedLabelRef.current);
        focusedLabelRef.current = null;
      }

      // Remove all planet labels
      planetLabelsRef.current.forEach(label => {
        if (label.parent) label.parent.remove(label);
      });
      planetLabelsRef.current = [];

      focusedStarRef.current = null;
      focusLight.visible = false;

      starGroup.visible = true;
      starfield.visible = true;

      clearGroup(focusGroup);
      clearGroup(planetGroup);

      scene.fog = new THREE.FogExp2(0x01010f, 0.00015);

      // Hide all star labels
      starGroup.children.forEach(s => {
        if (s.userData.label) s.userData.label.visible = false;
      });

      camera.position.copy(new THREE.Vector3(0, 200, 1200));
      controls.target.set(0, 0, 0);
      controls.minDistance = 10;
      controls.maxDistance = 80000;
      controls.update();
    };

    const focusOnStar = async (clickedStar) => {
      if (!clickedStar || !clickedStar.userData) return;

      focusedStarRef.current = clickedStar;

      starGroup.visible = false;
      starfield.visible = false;

      clearGroup(focusGroup);
      clearGroup(planetGroup);

      scene.fog = null;

      const starData = clickedStar.userData.starData;
      const originalRadius = clickedStar.userData.originalRadius;
      const scaleFactor = 8;

      // Focused star
      const focusedStarGeom = new THREE.SphereGeometry(originalRadius * scaleFactor, 32, 32);
      const focusedStarMat = new THREE.MeshPhongMaterial({ 
        emissive: 0xffaa00, 
        color: 0xffffcc, 
        emissiveIntensity: 1.2,
        shininess: 100
      });
      const focusedStar = new THREE.Mesh(focusedStarGeom, focusedStarMat);
      focusedStar.position.set(0, 0, 0);

      // Glow
      const glowGeom = new THREE.SphereGeometry(originalRadius * scaleFactor * 1.3, 32, 32);
      const glowMat = new THREE.MeshBasicMaterial({ 
        color: 0xffffaa, 
        transparent: true, 
        opacity: 0.3, 
        blending: THREE.AdditiveBlending 
      });
      const glow = new THREE.Mesh(glowGeom, glowMat);
      focusedStar.add(glow);

      // Focused label
      const labelDiv = document.createElement("div");
      labelDiv.textContent = starData.name || "Star";
      labelDiv.style.color = "#fff";
      labelDiv.style.fontSize = "18px";
      labelDiv.style.padding = "6px 12px";
      labelDiv.style.background = "rgba(0,0,0,0.8)";
      labelDiv.style.borderRadius = "6px";
      labelDiv.style.fontWeight = "bold";
      labelDiv.style.border = "2px solid #ffaa00";
      labelDiv.style.pointerEvents = "none";
      const focusedLabel = new CSS2DObject(labelDiv);
      focusedLabel.position.set(0, originalRadius * scaleFactor * 1.5, 0);
      focusedStar.add(focusedLabel);
      focusedLabelRef.current = focusedLabel;

      focusGroup.add(focusedStar);

      focusLight.position.set(0, 100, 100);
      focusLight.visible = true;

      const cameraDistance = originalRadius * scaleFactor * 30;
      camera.position.set(0, cameraDistance * 0.3, cameraDistance);
      controls.target.set(0, 0, 0);
      controls.minDistance = originalRadius * scaleFactor * 2;
      controls.maxDistance = cameraDistance * 3;
      controls.update();

      // Fetch planets
      if (fetchPlanetsForStar) {
        try {
          const planets = await fetchPlanetsForStar(starData);
          if (planets && planets.length > 0) {
            planets.forEach((p, index) => {
              const baseDistance = originalRadius * scaleFactor * 3;
              const distance = p.semi_major_axis 
                ? baseDistance + Math.log(p.semi_major_axis + 1) * 20 
                : baseDistance + (index + 1) * 30;

              const angle = (index / planets.length) * 2 * Math.PI;
              const px = distance * Math.cos(angle);
              const py = (Math.random() - 0.5) * 20;
              const pz = distance * Math.sin(angle);

              const planetRadius = p.radius 
                ? Math.max(Math.log(p.radius + 1) * 3, 2) 
                : 2;

              const planetGeom = new THREE.SphereGeometry(planetRadius, 24, 24);
              const planetMat = new THREE.MeshStandardMaterial({ 
                color: 0x3399ff, 
                metalness: 0.6, 
                roughness: 0.3,
                emissive: 0x0066cc,
                emissiveIntensity: 0.4
              });
              const planetMesh = new THREE.Mesh(planetGeom, planetMat);
              planetMesh.position.set(px, py, pz);

              const orbitGeom = new THREE.RingGeometry(distance - 1, distance + 1, 64);
              const orbitMat = new THREE.MeshBasicMaterial({ 
                color: 0x4488ff, 
                side: THREE.DoubleSide, 
                transparent: true, 
                opacity: 0.4 
              });
              const orbit = new THREE.Mesh(orbitGeom, orbitMat);
              orbit.rotation.x = Math.PI / 2;
              planetGroup.add(orbit);

              // Planet label
              const planetLabelDiv = document.createElement("div");
              planetLabelDiv.textContent = p.name || `Planet ${index + 1}`;
              planetLabelDiv.style.color = "#88ddff";
              planetLabelDiv.style.fontSize = "14px";
              planetLabelDiv.style.padding = "3px 8px";
              planetLabelDiv.style.background = "rgba(0,40,80,0.9)";
              planetLabelDiv.style.borderRadius = "4px";
              planetLabelDiv.style.border = "1px solid #4488cc";
              planetLabelDiv.style.pointerEvents = "none";
              const planetLabel = new CSS2DObject(planetLabelDiv);
              planetLabel.position.set(0, planetRadius * 1.5, 0);
              planetMesh.add(planetLabel);

              planetLabelsRef.current.push(planetLabel);

              planetGroup.add(planetMesh);
            });
          }
        } catch (error) {
          console.error("Error fetching planets:", error);
        }
      }
    };

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const onClick = async (event) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
      raycaster.setFromCamera(mouse, camera);

      if (focusedStarRef.current) {
        resetView();
        return;
      }

      const intersects = raycaster.intersectObjects(starGroup.children);
      if (intersects.length > 0) {
        await focusOnStar(intersects[0].object);
      }
    };

    let mouseDownPos = new THREE.Vector2();
    let mouseDownTime = 0;

    const onMouseDown = (event) => {
      mouseDownPos.set(event.clientX, event.clientY);
      mouseDownTime = performance.now();
    };

    const onMouseUp = (event) => {
      const mouseUpPos = new THREE.Vector2(event.clientX, event.clientY);
      const distance = mouseDownPos.distanceTo(mouseUpPos);
      const timeDiff = performance.now() - mouseDownTime;
      if (distance < 5 && timeDiff < 250) onClick(event);
    };

    renderer.domElement.addEventListener("mousedown", onMouseDown);
    renderer.domElement.addEventListener("mouseup", onMouseUp);

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();

      if (starfield.visible) starfield.rotation.y += 0.00005;

      planetGroup.children.forEach((child) => {
        if (child.type === 'Mesh' && child.geometry.type === 'SphereGeometry') {
          child.rotation.y += 0.01;
        }
      });

      if (focusGroup.children.length > 0) focusGroup.children[0].rotation.y += 0.002;

      renderer.render(scene, camera);
      labelRenderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      camera.aspect = currentMount.clientWidth / currentMount.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
      labelRenderer.setSize(currentMount.clientWidth, currentMount.clientHeight);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      renderer.domElement.removeEventListener("mousedown", onMouseDown);
      renderer.domElement.removeEventListener("mouseup", onMouseUp);
      if (currentMount) {
        if (renderer.domElement.parentNode === currentMount) currentMount.removeChild(renderer.domElement);
        if (labelRenderer.domElement.parentNode === currentMount) currentMount.removeChild(labelRenderer.domElement);
      }
      renderer.dispose();
    };
  }, [stars, fetchPlanetsForStar]);

  return <div ref={mountRef} style={{ width: "100%", height: "100%" }} />;
}
